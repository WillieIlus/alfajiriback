from django.urls import path

from .views import (CompanyListCreateAPIView, CompanyRetrieveUpdateDestroyAPIView, CompanyUserViewSet, CompanyLocationViewSet, CompanyCategoryViewSet)

app_name = 'companies'

urlpatterns = [
    path('', CompanyListCreateAPIView.as_view(), name='list_create'),
    path('<slug:slug>/', CompanyRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy'),
    # path('user/<int:user_id>/', CompanyUserViewSet.as_view({'get'}), name='user_list'),
    # path('location/<slug:location_slug>/', CompanyLocationViewSet.as_view({'get'}), name='location_list'),
    # path('category/<slug:category_slug>/', CompanyCategoryViewSet.as_view({'get'}), name='category_list'),
    ]
