import csv

from django.core.management.base import BaseCommand, CommandError

from models import Door


class Command(BaseCommand):
    help = 'Загружает все записи из CSV файла в базу данных'

    def handle(self, *args, **kwargs):
        csv_file = 'doors_data.csv'

        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0

                for row in reader:
                    if not Door.objects.filter(title=row['title']).exists():
                        Door.objects.create(
                            title=row['title'],
                            article=row['article'],
                            price=row['price'],
                            purpose=row['purpose'],
                            conturs_name=row['contursName'],
                            size_name=row['sizeName'],
                            steel_size=row['steelSize'],
                            tolshina=row['tolshina'],
                            korob_size=row['korobSize'],
                            uteplitel=row['uteplitel'],
                            ves=row['ves'],
                            constr_korob=row['constrKorob'],
                            constr_fixator=row['constrFixator'],
                            zamok1=row['zamok1'],
                            zamok2=row['zamok2'],
                            furn_color_name=row['furnColorName'],
                            petli=row['petli'],
                            zadvijka=row['zadvijka'],
                            ruchka=row['ruchka'],
                            glazok=row['glazok'],
                            cilindr=row['cilindr'],
                            bronia=row['bronia'],
                            out_cover_name=row['outCoverName'],
                            out_color=row['outColor'],
                            in_cover_name=row['inCoverName'],
                            in_thick=row['inThick'],
                            in_color=row['inColor'],
                            images=row['images']
                        )
                        count += 1
                        if count % 500 == 0:
                            self.stdout.write(self.style.SUCCESS(f'Загружено записей: {count}'))

            self.stdout.write(self.style.SUCCESS(f'Все записи успешно загружены из {csv_file}. Всего записей: {count}'))

        except FileNotFoundError:
            raise CommandError(f'Файл {csv_file} не найден')

        except Exception as e:
            raise CommandError(f'Ошибка при загрузке данных: {e}')
