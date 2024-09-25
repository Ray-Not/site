import requests
from bs4 import BeautifulSoup
import time
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from slugify import slugify
import os

base_url = 'https://doors007.ru/doors.html'
base_dir = 'https://doors007.ru/'
headers = {
    'User-Agent': 'SomeName/1.0 (+http://some.com/bot)'
}

# Настройка сессии с повторными запросами
session = requests.Session()
retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def get_with_retries(url, retries=5, delay=2):
    """Функция для выполнения GET-запросов с повторными попытками."""
    for i in range(retries):
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()  # Проверка на ошибки
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка: {e}. Попытка {i + 1} из {retries}.")
            time.sleep(delay)  # Ждать перед повторной попыткой
    return None  # Возвращает None, если не удалось выполнить запрос


total_pages = 277
with open('doors_data.csv', 'a+', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'equipment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for page in range(0, total_pages + 1):
        print(f"Парсинг страницы {page} из {total_pages}...")
        url = f'{base_url}?page={page}&fndtype=steel'

        # Получение основной страницы с повторными попытками
        response = session.get(url, headers=headers, timeout=100)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='product')

            for product in products:
                thumb = product.find('div', class_='thumb')
                link_tag = thumb.find('a') if thumb else None
                link = link_tag['href'] if link_tag else 'Нет ссылки'
                if link == 'Нет ссылки':
                    continue
                
                # Получение страницы продукта с повторными попытками
                product_response = session.get(link, headers=headers)
                if product_response.status_code == 200:
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')
                    title = slugify(product_soup.find('h1', class_='product_name').text.strip()) if product_soup.find('h1', class_='product_name') else 'Нет информации'
                    product_dir = os.path.join('media/doors_equip', title)
                    os.makedirs(product_dir, exist_ok=True)

                    # Используем множество для хранения уникальных элементов оборудования
                    equipment_set = set()
                    equipment_section = product_soup.find('section', class_='product_equipment block')
                    if equipment_section:
                        equipment_buttons = equipment_section.find_all('button', class_='item')
                        for button in equipment_buttons:
                            type_label = button.find('div', class_='type').text.strip() if button.find('div', class_='type') else 'Нет информации'
                            name_label = button.find('div', class_='name').text.strip() if button.find('div', class_='name') else 'Нет информации'
                            img_src = button.find('img', class_='lozad')
                            img_url = img_src['data-src'] if img_src and img_src.has_attr('data-src') else 'Нет изображения'

                            # Загрузка изображения с повторными попытками
                            if img_url != 'Нет изображения':
                                img_response = get_with_retries(img_url)
                                if img_response:
                                    # Получаем имя файла из URL
                                    parts = img_url.split('/')
                                    img_name = f"{parts[-4]}_{parts[-3]}_{parts[-2]}_{parts[-1].split('.')[0]}.jpg"
                                    img_path = os.path.join(product_dir, img_name)
                                    img_url = img_path
                                    # Сохраняем изображение
                                    with open(img_path, 'wb') as img_file:
                                        img_file.write(img_response.content)
                                        print(f"Изображение сохранено: {img_path}")

                            # Добавляем уникальные элементы в множество
                            equipment_set.add(f"{type_label}: {name_label}, {img_url}")

                    # Преобразуем множество обратно в строку
                    equipment_str = '; '.join(equipment_set) if equipment_set else 'Нет информации'

                    writer.writerow({
                        'title': title,
                        'equipment': equipment_str
                    })

                    print(f"Title: {title}, Equipment: {equipment_str}")
                    time.sleep(2)
                else:
                    print(f"Ошибка: не удалось получить доступ к продукту по ссылке {link} (статус код {product_response.status_code})")
        else:
            print(f"Ошибка: не удалось получить доступ к странице {page} (статус код {response.status_code})")

        time.sleep(5)
