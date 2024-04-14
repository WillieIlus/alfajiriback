from django.urls import path

from .views import (CompanyListCreateAPIView, CompanyRetrieveUpdateDestroyAPIView, CategoryCompanyViewSet,
                    MyCompanyViewSet, CompanyLocationViewSet, CompanyCategoryViewSet)

app_name = 'companies'

urlpatterns = [
    path('my/', MyCompanyViewSet.as_view(), name='user_list'),
    path('', CompanyListCreateAPIView.as_view(), name='list_create'),
    path('<slug:slug>/', CompanyRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy'),
    path('category/<slug:slug>/', CategoryCompanyViewSet.as_view(), name='category_list'),

    # path('user/<int:user_id>/', MyCompanyViewSet.as_view({'get'}), name='user_list'),
    # path('location/<slug:location_slug>/', CompanyLocationViewSet.as_view({'get'}), name='location_list'),
    # path('category/<slug:category_slug>/', CompanyCategoryViewSet.as_view({'get'}), name='category_list'),
]
