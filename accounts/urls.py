from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserDetailRetrieveUpdateDestroyView

app_name = 'accounts'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('me/', UserDetailRetrieveUpdateDestroyView.as_view(), name='user-detail'),
]