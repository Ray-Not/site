import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from slugify import slugify


class BlogChapter(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='chapter')
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, separator='-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=255)
    chapter = models.ForeignKey(
        BlogChapter,
        on_delete=models.CASCADE,
        related_name='blogs'
    )
    content = RichTextField()
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, separator='-')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post_detail', args=[self.chapter.slug, self.slug])

    def __str__(self):
        return self.title


class DeliveryRegion(models.Model):

    REGION_CHOICES = [
        ('moscow', 'Москва'),
        ('moscow_region', 'Московская область'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='delivery_region',
        blank=True
    )
    slug = models.SlugField(max_length=255, unique=True)
    region = models.CharField(
        max_length=20,
        choices=REGION_CHOICES,
        default='moscow_region',
        verbose_name='Регион'
    )
    text = models.TextField(blank=True)
    cost = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, separator='-')
        super().save(*args, **kwargs)

    class Meta:
        pass


class CallBack(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=18)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(CallBack, self).save(*args, **kwargs)  # Сначала сохраняем объект

            # Отправка email уведомления
            send_mail(
                'Обратный звонок',
                f'Была создана новая заявка [обратный вызов] от {self.name}.\nТелефон: {self.phone}',
                settings.DEFAULT_FROM_EMAIL,  # От кого
                ['4109974@inbox.ru'],  # Кому отправляем (ваша же почта)
                fail_silently=False,
            )
        else:
            super(CallBack, self).save(*args, **kwargs)


class Catalog(models.Model):
    title = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to='catalog',
        null=True,
        blank=True
    )
    description = models.CharField(max_length=150, null=True, blank=True)
    content = models.TextField(default='')
    custom_h1 = models.CharField(max_length=256, default='Входные металлические {{ catalog.title|lower }} двери')
    custom_title = models.CharField(max_length=150, null=True, blank=True)

    def get_door_count(self):
        """Возвращает количество дверей, связанных с данной категорией."""
        return self.catalogs.count()

    def get_absolute_url(self):
        return reverse('catalog_with_slug', kwargs={'slug': self.slug})

    def __str__(self) -> str:
        return f"{self.title} из '{self.chapter}'"


class Tag(models.Model):
    TEXT_COLOR_CHOICES = [
        ('dark', 'Dark'),
        ('light', 'Light'),
    ]

    text_color = models.CharField(
        max_length=10,
        choices=TEXT_COLOR_CHOICES,
        default='dark',
        help_text='Выбор цвета текста'
    )
    title = models.CharField(max_length=255, unique=True)
    color_hex = models.CharField(
        max_length=7,
        help_text='Введите цвет в формате #RRGGBB'
    )

    def __str__(self) -> str:
        return f"{self.title} [{self.color_hex}]"


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(11)]

    name = models.CharField(max_length=255)
    order = models.OneToOneField(
        'Order',
        on_delete=models.CASCADE,
        related_name='review',
        null=True
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    message = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'От {self.name} [{self.order}]: Рейтинг {self.rating}'


class Door(models.Model):
    title = models.CharField(max_length=255)
    article = models.CharField(max_length=255)
    price = models.IntegerField()
    purpose = models.CharField(max_length=255)
    conturs_name = models.CharField(max_length=255)
    size_name = models.CharField(max_length=255)
    steel_size = models.CharField(max_length=255)
    tolshina = models.CharField(max_length=255)
    korob_size = models.CharField(max_length=255)
    uteplitel = models.CharField(max_length=255)
    ves = models.CharField(max_length=255)
    constr_korob = models.CharField(max_length=255)
    constr_fixator = models.CharField(max_length=255)
    zamok1 = models.CharField(max_length=255)
    zamok2 = models.CharField(max_length=255)
    furn_color_name = models.CharField(max_length=255)
    petli = models.CharField(max_length=255)
    zadvijka = models.CharField(max_length=255)
    ruchka = models.CharField(max_length=255)
    glazok = models.CharField(max_length=255)
    cilindr = models.CharField(max_length=255)
    bronia = models.CharField(max_length=255)
    out_cover_name = models.CharField(max_length=255)
    out_color = models.CharField(max_length=255)
    in_cover_name = models.CharField(max_length=255)
    in_thick = models.CharField(max_length=255)
    in_color = models.CharField(max_length=255)
    images = models.TextField()
    discount = models.PositiveSmallIntegerField(null=True, default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='doors', blank=True)
    catalogs = models.ManyToManyField(
        Catalog,
        related_name='catalogs',
        blank=True
    )
    equipment = models.CharField(max_length=1024*1024)
    description = models.CharField(max_length=255, blank=True)
    catalogs_cloud = models.ManyToManyField(
        Catalog,
        related_name='catalogs_cloud',
        blank=True
    )
    hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    h1 = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=512, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, separator='-')
            self.slug = slug
        if not self.description:
            self.description = f'Купить дверь {self.title}, недорого'
        super().save(*args, **kwargs)

    def get_reviews(self):
        """Возвращает все отзывы, связанные с дверью через заказы."""
        return Review.objects.filter(order__door=self)

    def get_order_count(self):
        return self.orders.count()

    def get_absolute_url(self):
        return reverse('door_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Order(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    call_time = models.DateTimeField()
    address = models.CharField(max_length=512)
    message = models.TextField()
    order_number = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
        blank=True
    )
    door = models.ForeignKey(
        'Door',
        on_delete=models.CASCADE,
        related_name='orders',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_unique_order_number()

        if self.pk is None:
            super(Order, self).save(*args, **kwargs)  # Сначала сохраняем объект

            message = f'Была создана новая заявка от {self.name}.\nТелефон: {self.phone}\nАдрес: {self.address}\nСообщение: {self.message}'
            title = 'Вызов на замер'
            if self.door:
                message += f'\nДверь: {self.door.title}.'
                title = "Новый заказ"

            # Отправка email уведомления
            send_mail(
                title,
                message,
                settings.DEFAULT_FROM_EMAIL,  # От кого
                ['4109974@inbox.ru'],  # Кому отправляем (ваша же почта)
                fail_silently=False,
            )
        else:
            super(Order, self).save(*args, **kwargs)

    def generate_unique_order_number(self):
        while True:
            order_number = f'ORD-{uuid.uuid4().hex[:8]}'
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def __str__(self):
        return f'От {self.name} ({self.phone}) пришел заказ \
            [{self.order_number}]: {self.message}'


class CustomOrder(models.Model):

    construct_choices = [
        ('0', '1 лист 2 мм + 1 контур уплотнения'),
        ('1', '1 лист 3 мм + 1 контур уплотнения'),
        ('2', '1 лист 4 мм + 1 контур уплотнения'),
        ('3', '2 листа 2 мм + 2 контура уплотнения'),
        ('4', '2 листа 3 мм + 2 контура уплотнения'),
        ('5', '2 листа 4 мм + 2 контура уплотнения'),
        ('1.6', 'Цельноугольный лист 1.5 мм + полотно 70 мм'),
        ('7', 'Цельноугольный лист 1.5 мм, противосъемная'),
        ('8', 'Противопожарная'),
    ]

    glazing_choices = [
        ('0', 'Нет'),
        ('1', 'Однокамерный'),
        ('2', 'Двухкамерный'),
        ('3', 'Трехкамерный'),
    ]

    cover_choices = [
        ('0', 'Нет'),
        ('1', 'Нитроэмаль'),
        ('2', 'Искусственная кожа'),
        ('3', 'Вагонка'),
        ('4', 'Порошковое напыление'),
        ('5', 'Ламинат-панель'),
        ('6', 'Панель МДФ 10 мм сплошная'),
        ('7', 'МДФ-плита 10 мм сплошная'),
        ('9', 'МДФ-плита 12+ мм с рисунком'),
        ('10', 'МДФ-плита 12+ мм с полноразмерной фрезеровкой'),
        ('11', 'МДФ-плита 12+ мм окрашенная с фрезеровкой'),
        ('12', 'Массив дуба'),
        ('13', 'Массив дуба с фрезеровкой'),
    ]

    platbans_choices = [
        ('0', 'Нет'),
        ('1', 'Наличник металлический гнутый'),
        ('2', 'Наличник из МДФ'),
        ('3', 'Наличник из массива дуба'),
    ]

    bot_castle_choices = [
        ('0', 'Нет'),
        ('1', 'Apecs 1900-INOX врезной, противопожарный'),
        ('2', 'Эльбор 1.05.41 сувальдный, ручка + задвижка'),
        ('3', 'Apecs T-05-CR, цилиндровый, ручка на общей планке'),
        ('4', 'Apecs 2000-Panic-ZN врезной, противопожарный'),
        ('5', 'МЕТТЭМ 3В4 713.0.0 цилиндровый (Apecs), без ручки'),
        ('6', 'МЕТТЭМ 3В9 144.0.0 сувальдный под ночную задвижку'),
        ('7', 'МЕТТЭМ 3В9 343.1.1 сувальдный (без перекодировки)'),
        ('8', 'МЕТТЭМ 3В9 143 сувальдный под ручку без ночной задвижки'),
        ('9', 'Kale 252R (с броненакладкой)'),
        ('10', 'Kale 257RL, сувальдный'),
        ('11', 'Гардиан 30.11, сувальдный'),
        ('12', 'Гардиан 32.11, цилиндровый'),
        ('13', 'Гардиан 22.12Т, цилиндровый'),
        ('14', 'Гардиан 25.14, двухсистемый'),
        ('15', 'Гардиан 32.01, цилиндровый'),
        ('16', 'Гардиан 21.12, сувальдный'),
        ('17', 'Гардиан 40.11, сувальдный'),
        ('18', 'Гардиан 75.14, двухсистемный'),
        ('19', 'Гардиан 12.14.ДТ, сувальдный'),
        ('17', 'Cisa 57.986, двухсистемный'),
        ('18', 'Cisa 57.535, сувальдный + ручка'),
        ('19', 'Cisa 56.535, цилиндровый + ручка'),
    ]

    top_castle_choices = [
        ('0', 'Нет'),
        ('1', 'CAM 3B8-8M'),
        ('2', 'ЭЛЬБОР 1.05.01, сувальдный'),
        ('3', 'CRIT, цилиндровый'),
        ('4', 'Kale 257, цилиндровый'),
        ('5', 'Kale 257L, сувальдный'),
        ('6', 'KERBEROS 115'),
        ('7', 'KERBEROS 3'),
        ('8', 'KERBEROS 6'),
        ('9', 'KERBEROS 9й серии'),
        ('10', 'Гардиан 30.01, сувальдный'),
        ('11', 'Гардиан 50.01, сувальдный'),
        ('12', 'Гардиан 32.01 цилиндровый'),
        ('13', 'Cisa 57.525, сувальдный'),
        ('14', 'Cisa 57.675, сувальдный'),
        ('15', 'Cisa 56.525, цилинровый'),
        ('16', 'МЕТТЭМ 3В1 711.0.0, цилиндровый'),
        ('17', 'МЕТТЭМ 3В8 160.0.0, сувальдный'),
        ('18', 'МЕТТЭМ 3В8 611.0.1, сувальдный'),
        ('19', 'МЕТТЭМ 3В7 Т-П, цилиндровый'),
        ('20', 'Кодовый замок'),
        ('21', 'Биометрический замок (отпечаток пальца)'),
        ('22', 'Биометрический замок (лицо)'),
    ]

    cylinder_choices = [
        ('0', 'Нет'),
        ('1', 'Fuaro с перфорацией'),
        ('2', 'Apecs с перфорацией'),
        ('3', 'Kale с перфорацией'),
        ('4', 'Cisa Asics'),
        ('5', 'Cisa Astral'),
        ('6', 'Cisa AP3'),
        ('7', 'EVVA ICS'),
        ('8', 'CISA RS3'),
        ('9', 'EVVA 3KS'),
    ]

    hinge_choices = [
        ('0', 'На подшипнике, 2 шт.'),
        ('1', 'На подшипнике, 3 шт.'),
        ('2', 'На подшипнике, 4 шт.'),
        ('3', 'На подшипнике, 5 шт.'),
        ('4', 'На подшипнике, 6 шт.'),
    ]

    blockers_choices = [
        ('0', 'Нет'),
        ('1', 'Блокираторы конусный, 2 шт.'),
        ('2', 'Блокираторы конусный, 3 шт.'),
        ('3', 'Блокираторы конусный, 4 шт.'),
    ]

    insulation_choices = [
        ('0', 'Нет'),
        ('1', 'ISOVER'),
        ('2', 'ROCKWOOL'),
    ]

    dismantling_choices = [
        ('0', 'Нет'),
        ('1', 'Деревянная дверь одностворчатая'),
        ('2', 'Металлическая дверь одностворчатая'),
        ('3', 'Деревянная дверь полуторная / двустворчатая'),
        ('4', 'Металлическая дверь полуторная / двустворчатая'),
    ]

    phone = models.CharField(max_length=30)
    height = models.DecimalField(decimal_places=0, max_digits=10)
    width = models.DecimalField(decimal_places=0, max_digits=10)
    type_contruction = models.CharField(
        max_length=64,
        choices=construct_choices,
        default='0',
        verbose_name='Тип конструкции'
    )
    double_glazing = models.CharField(
        max_length=32,
        choices=glazing_choices,
        default='0',
        verbose_name='Стеклопакет'
    )
    out_cover = models.CharField(
        max_length=128,
        choices=cover_choices,
        default='0',
        verbose_name='Отделка снаружи'
    )
    in_cover = models.CharField(
        max_length=128,
        choices=cover_choices,
        default='0',
        verbose_name='Отделка внутри'
    )
    platbans = models.CharField(
        max_length=64,
        choices=platbans_choices,
        default='0',
        verbose_name='Наличники'
    )
    top_castle = models.CharField(
        max_length=64,
        choices=top_castle_choices,
        default='0',
        verbose_name='Нижний замок'
    )
    bot_castle = models.CharField(
        max_length=64,
        choices=bot_castle_choices,
        default='0',
        verbose_name='Верхний замок'
    )
    cylinder = models.CharField(
        max_length=32,
        choices=cylinder_choices,
        default='0',
        verbose_name='Целиндр'
    )
    hinge = models.CharField(
        max_length=32,
        choices=hinge_choices,
        default='0',
        verbose_name='Петли'
    )
    blockers = models.CharField(
        max_length=64,
        choices=blockers_choices,
        default='0',
        verbose_name='Блокираторы'
    )
    insulation = models.CharField(
        max_length=32,
        choices=insulation_choices,
        default='0',
        verbose_name='Утеплитель'
    )
    dismantling = models.CharField(
        max_length=32,
        choices=dismantling_choices,
        default='0',
        verbose_name='Демонтаж'
    )
    night_lock = models.BooleanField(
        default=False,
        verbose_name='Ночная задвижка'
    )
    peephole = models.BooleanField(
        default=False,
        verbose_name='Глазок'
    )
    door_closer_100kg = models.BooleanField(
        default=False,
        verbose_name='Доводчик до 100 кг'
    )
    door_closer_120kg = models.BooleanField(
        default=False,
        verbose_name='Доводчик до 120 кг'
    )
    handle_scarf = models.BooleanField(
        default=False,
        verbose_name='Ручка-скоба'
    )

    def save(self, *args, **kwargs):

        if self.pk is None:
            super(CustomOrder, self).save(*args, **kwargs)

            message = f'Заявка на персональную дверь.\nТелефон: {self.phone}.'

            # Отправка email уведомления
            send_mail(
                'Заказ по параметрам',
                message,
                settings.DEFAULT_FROM_EMAIL,  # От кого
                ['4109974@inbox.ru'],  # Кому отправляем (ваша же почта)
                fail_silently=False,
            )
        else:
            super(CustomOrder, self).save(*args, **kwargs)

    def __str__(self):
        return f'От {self.phone} пришел заказ'


class GetDiscount(models.Model):
    phone = models.CharField(max_length=32)

    def save(self, *args, **kwargs):

        if self.pk is None:
            super(GetDiscount, self).save(*args, **kwargs)

            message = f'Заявка на скидку.\nТелефон: {self.phone}.'
            # Отправка email уведомления
            send_mail(
                'Получение скидки',
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['4109974@inbox.ru'],
                fail_silently=False,
            )
        else:
            super(GetDiscount, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.phone} нужна скидка"
