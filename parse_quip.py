import csv
import hashlib
import os
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from slugify import slugify

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

def get_with_retries(url, retries=10, delay=2):
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

def is_cached(file_path):
    """Проверяет, существует ли файл (используется для кэширования изображений)."""
    return os.path.exists(file_path)

def save_image_to_cache(img_url, product_dir):
    """Загрузка и сохранение изображения с кэшированием."""
    # Проверяем, является ли URL относительным
    if not img_url.startswith('http'):
        img_url = base_dir + img_url.lstrip('/')  # Преобразуем относительный URL в абсолютный

    parts = img_url.split('/')
    img_name = f"{parts[-4]}_{parts[-3]}_{parts[-2]}_{parts[-1].split('.')[0]}.jpg"
    img_path = os.path.join(product_dir, img_name)

    if is_cached(img_path):
        print(f"Изображение уже в кэше: {img_path}")
        return img_path  # Возвращаем путь к существующему файлу

    img_response = get_with_retries(img_url)
    if img_response:
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f"Изображение сохранено: {img_path}")
        return img_path
    else:
        print(f"Не удалось загрузить изображение: {img_url}")
        return 'Нет изображения'

def load_existing_data(csv_file):
    """Чтение существующих данных из CSV файла."""
    existing_data = set()
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Используем хэш заголовка и оборудования для уникальности записей
                record_hash = hashlib.md5(f"{row['title']}{row['equipment']}".encode('utf-8')).hexdigest()
                existing_data.add(record_hash)
    return existing_data

def process_product(product, headers, existing_data):
    """Функция для обработки одного продукта."""
    thumb = product.find('div', class_='thumb')
    link_tag = thumb.find('a') if thumb else None
    link = link_tag['href'] if link_tag else 'Нет ссылки'

    if link == 'Нет ссылки':
        return None

    product_response = session.get(link, headers=headers)
    if product_response.status_code != 200:
        print(f"Ошибка: не удалось получить доступ к продукту по ссылке {link} (статус код {product_response.status_code})")
        return None

    product_soup = BeautifulSoup(product_response.text, 'html.parser')
    title = slugify(product_soup.find('h1', class_='product_name').text.strip()) if product_soup.find('h1', class_='product_name') else 'Нет информации'
    equipment_set = set()
    equipment_section = product_soup.find('section', class_='product_equipment block')
    if equipment_section:
        equipment_buttons = equipment_section.find_all('button', class_='item')
        for button in equipment_buttons:
            type_label = button.find('div', class_='type').text.strip() if button.find('div', class_='type') else 'Нет информации'
            name_label = button.find('div', class_='name').text.strip() if button.find('div', class_='name') else 'Нет информации'
            img_src = button.find('img', class_='lozad')
            img_url = img_src['data-src'] if img_src and img_src.has_attr('data-src') else 'Нет изображения'

            if img_url != 'Нет изображения':
                equipment_set.add(f"{type_label}: {name_label}")

    equipment_str = '; '.join(equipment_set) if equipment_set else 'Нет информации'

    # Проверяем, существует ли запись
    record_hash = hashlib.md5(f"{title}{equipment_str}".encode('utf-8')).hexdigest()
    if record_hash in existing_data:
        print(f"Запись уже существует: {title}")
        return None
    else:
        return {'title': title, 'equipment': equipment_str}

def process_page(page, writer, existing_data):
    """Обрабатывает одну страницу."""
    url = f'{base_url}?page={page}&fndtype=steel'
    response = session.get(url, headers=headers, timeout=100)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_='product')

        for product in products:
            result = process_product(product, headers, existing_data)
            if result:
                writer.writerow(result)
    else:
        print(f"Ошибка: не удалось получить доступ к странице {page} (статус код {response.status_code})")

total_pages = 277
csv_file = 'doors_data_default.csv'

# Загружаем уже существующие данные
existing_data = load_existing_data(csv_file)

with open(csv_file, 'a+', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'equipment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not os.path.exists(csv_file) or os.stat(csv_file).st_size == 0:
        writer.writeheader()  # Записываем заголовки, если файл пуст

    # Последовательная обработка страниц
    for page in range(0, total_pages + 1):
        process_page(page, writer, existing_data)
