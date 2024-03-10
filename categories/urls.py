from django.urls import path

from .views import CategoryListAPIView, CategoryDetailAPIView


urlpatterns = [
    path('', CategoryListAPIView.as_view(), name='list'),
    path('<slug:category_slug>/', CategoryDetailAPIView.as_view(), name='detail'),
]