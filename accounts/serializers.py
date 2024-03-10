from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'avatar', 'role', 'bio', 'phone', 'is_staff', 'is_active', 'date_joined', 'last_login', 'address')
        read_only_fields = ('id', 'is_staff', 'is_active', 'date_joined', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}
