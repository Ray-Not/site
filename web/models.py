import uuid

from django.db import models
from django.forms import ValidationError
from slugify import slugify


class Tag(models.Model):
    title = models.CharField(max_length=255)
    color = models.CharField(
        max_length=7,
        help_text='Введите цвет в формате #RRGGBB'
    )
    in_cloud = models.BooleanField(
        verbose_name='Добавление тэга в каталог категорий'
    )

    def __str__(self) -> str:
        return f"{self.title} [{self.color_hex}]"


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(11)]

    name = models.CharField(max_length=255)
    order = models.OneToOneField(
        'Order',
        on_delete=models.CASCADE,
        related_name='review'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    message = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.order.door:
            raise ValidationError(
                'Отзыв можно оставить только на заказ, связанный с дверью.'
            )
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, separator='-')
            self.slug = slug
        super().save(*args, **kwargs)

    def get_reviews(self):
        """Возвращает все отзывы, связанные с дверью через заказы."""
        return Review.objects.filter(order__door=self)

    def get_order_count(self):
        return self.orders.count()

    def __str__(self):
        return self.title


class Order(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    call_time = models.DateTimeField()
    address = models.TextField()
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
        super().save(*args, **kwargs)

    def generate_unique_order_number(self):
        while True:
            order_number = f'ORD-{uuid.uuid4().hex[:8]}'
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def __str__(self):
        return f'От {self.name} ({self.phone}) пришел заказ \
            [{self.order_number}]: {self.message}'
