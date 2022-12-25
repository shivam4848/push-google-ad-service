from advertisement.Views.advertisement_views import AdvertisementView
from django.urls import path

urlpatterns = [
    path('get', AdvertisementView.as_view(), name='get_advertisement'),
    path('create', AdvertisementView.as_view(), name='create_advertisement'),
    path('update', AdvertisementView.as_view(), name='update_advertisement'),
    path('delete', AdvertisementView.as_view(), name='delete_advertisement')
]
