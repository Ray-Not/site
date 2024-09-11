from rest_framework import serializers

from api.models import Door, Order, Review, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class SearchDoorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Door
        fields = ['title', 'slug']


class DoorSerializer(serializers.ModelSerializer):

    reviews = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    def get_reviews(self, obj):
        reviews = Review.objects.filter(
            order__door=obj
        ).select_related('order')
        return ReviewSerializer(reviews, many=True).data

    class Meta:
        model = Door
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(write_only=True)
    order = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'name', 'rating', 'order_number', 'order']

    def get_order(self, obj):
        return obj.order.order_number if obj.order else None

    def validate(self, data):
        order_number = data.get('order_number')

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            raise serializers.ValidationError({
                'order_number': 'Заказ с таким номером не существует.'
            })

        if order.door is None:
            raise serializers.ValidationError({
                'order_number': 'Отзыв можно оставить только на \
заказ, связанный с дверью.'
            })

        if hasattr(order, 'review'):
            raise serializers.ValidationError({
                'order_number': 'Отзыв для этого заказа уже существует.'
            })

        return data

    def create(self, validated_data):
        order_number = validated_data.pop('order_number')
        order = Order.objects.get(order_number=order_number)
        validated_data['order'] = order
        return super().create(validated_data)
