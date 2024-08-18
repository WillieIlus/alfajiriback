from django.urls import path, include
from .views import UpdateUserProfileView, UserProfileView

app_name = 'accounts'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('profile/', UserProfileView.as_view(), name='profile-view'),
    path('profile/update/', UpdateUserProfileView.as_view(), name='profile-update'),
]