from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from api.models import Door, Review, Tag
from api.serializers import (DoorSerializer, ReviewSerializer,
                             SearchDoorSerializer, TagSerializer)

app_name = 'api'


class DoorPagination(PageNumberPagination):
    page_size = 3
    # page_size_query_param = 'page'
    # max_page_size = 100


class DoorRetrieveView(generics.RetrieveAPIView):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        try:
            return self.queryset.get(slug=slug)
        except Door.DoesNotExist:
            raise NotFound('Object not found')


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class DoorListView(generics.ListAPIView):
    queryset = Door.objects.all().order_by('id')
    serializer_class = DoorSerializer
    pagination_class = DoorPagination


class SearchDoorListView(generics.ListAPIView):
    queryset = Door.objects.all()
    serializer_class = SearchDoorSerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
