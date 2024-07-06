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
    user = UserSerializer(required=False)
    location = LocationSerializer(required=False)
    category = CategorySerializer(required=False)
    get_location = serializers.CharField(source='location', required=False)
    get_category = serializers.CharField(source='category', required=False)
    get_user = serializers.CharField(source='user', required=False)
    total_jobs = serializers.SerializerMethodField()
    jobs = JobSerializer(many=True, read_only=True)
    truncated_description = serializers.CharField(read_only=True)

    def get_total_jobs(self, company):
        return Job.objects.filter(company=company).count()

    class Meta:
        model = Company
        fields = 'id', 'name', 'slug', 'logo', 'total_jobs', 'website', 'truncated_description', 'description', 'job_count', 'get_user',\
            'user', 'jobs', 'address', 'get_location', 'location', 'get_category', 'category', 'created_at', 'updated_at'
        read_only_fields = ('slug', 'created_at', 'updated_at')
