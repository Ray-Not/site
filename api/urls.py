from django.urls import path

from api.views import (DoorListView, DoorRetrieveView, ReviewCreateView,
                       SearchDoorListView, TagListView)

urlpatterns = [
    path(
      'door/<slug:slug>/',
      DoorRetrieveView.as_view(),
      name='door-detail'
    ),
    path(
      'door/',
      DoorListView.as_view(),
      name='door-list'
    ),
    path(
      'review/',
      ReviewCreateView.as_view(),
      name='review-create'
    ),
    path(
      'search-door/',
      SearchDoorListView.as_view(),
      name='search-door-lise'
    ),
    path(
      'tags/',
      TagListView.as_view(),
      name='search-door-tag'
    ),
]
