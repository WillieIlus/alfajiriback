from django.urls import path

from .views import CountryList, CountryDetail, LocationList, LocationDetail

app_name = 'locations'

urlpatterns = [
    path('countries/', CountryList.as_view(), name='country_list'),
    path('countries/<slug:slug>/', CountryDetail.as_view(), name='country_detail'),
    path('locations/', LocationList.as_view(), name='location_list'),
    path('locations/<slug:slug>/', LocationDetail.as_view(), name='location_detail'),
]
