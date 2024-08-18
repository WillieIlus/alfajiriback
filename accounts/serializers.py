from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name', 'avatar', 'gender', 'address', 'city', 'phone', 'date_of_birth', 'bio', 'website']
        read_only_fields = ['email', 'id']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'avatar', 'gender', 'address', 'city', 'phone', 'date_of_birth', 'bio', 'website']