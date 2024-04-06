from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserListCreateView, UserDetailRetrieveUpdateDestroyView

app_name = 'accounts'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('<uuid:pk>/', UserDetailRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-delete'),
]
