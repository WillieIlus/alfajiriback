from rest_framework import serializers

from jobs.models import Job
from jobs.serializers import JobSerializer
from .models import Company

from accounts.models import User
from locations.models import Location
from categories.models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'phone'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = 'name', 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name', 'slug'


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    logo = serializers.ImageField(required=False)
    cover = serializers.ImageField(required=False)


    class Meta:
        model = Company
        fields = (
        'id', 'name', 'slug', 'logo', 'cover', 'phone', 'email', 'website', 'truncated_description', 'description',
        'job_count', 'user', 'address', 'location', 'category', 'created_at', 'updated_at')
        read_only_fields = ('slug', 'created_at', 'updated_at', 'user', 'location', 'category', 'job_count')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in ['description', 'phone', 'email', 'website', 'address']:
            if representation[field] is None:
                representation[field] = ''
        return representation

    def get_total_jobs(self, company):
        return Job.objects.filter(company=company).count()


