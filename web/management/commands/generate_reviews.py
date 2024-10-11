import csv
from django.core.management.base import BaseCommand
from web.models import Review  # Замените на вашу модель отзывов

class Command(BaseCommand):
    help = 'Присваивает отзывы из CSV файла в поле content объектов отзывов'

    def handle(self, *args, **kwargs):
        # Путь к файлу CSV
        csv_file_path = 'reviews.csv'

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                reviews = list(reader)

            review_objects = Review.objects.all()

            if len(reviews) < review_objects.count():
                self.stdout.write(self.style.WARNING('В CSV недостаточно отзывов для всех объектов, будут обновлены только доступные.'))

            for index, review_object in enumerate(review_objects):
                if index < len(reviews):
                    review_text = reviews[index][0]
                    review_object.message = review_text
                    review_object.save()
                    self.stdout.write(self.style.SUCCESS(f'Отзыв для объекта {review_object.id} обновлен.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Отзывов в CSV больше нет, пропущен объект {review_object.id}.'))
                    break

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл {csv_file_path} не найден'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {str(e)}'))
