import requests
from bs4 import BeautifulSoup
import csv

# URL для отзывов, где Pagen заменяем на конкретный номер страницы
url_template = 'https://belwood.kz/about/comments/?PAGEN_1={page}'

# Создаем CSV файл
with open('reviews.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Review'])  # Заголовок для колонки

    # Проходим по страницам
    for page in range(1, 51):  # Меняем Pagen от 1 до 50
        url = url_template.format(page=page)
        response = requests.get(url)

        if response.status_code == 200:  # Проверяем, успешен ли запрос
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим все элементы с отзывами
            reviews = soup.find_all('div', class_='feedback__text')

            # Записываем каждый отзыв в CSV
            for review in reviews:
                review_text = review.text.strip()
                writer.writerow([review_text])  # Записываем только текст отзыва
                print(f"Добавлен отзыв: {review_text[:60]}...")  # Печать первых 60 символов для проверки
        else:
            print(f"Ошибка при запросе страницы {page}, код: {response.status_code}")

print("Все отзывы сохранены в reviews.csv")
