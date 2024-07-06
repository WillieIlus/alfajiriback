from rest_framework import serializers

from .models import Job, JobApplication, Impression, Click, Bookmark

from accounts.models import User
from companies.models import Company
from locations.models import Location
from categories.models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'phone'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = 'id', 'name', 'slug', 'logo', 'website', 'description'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = 'id', 'name', 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name', 'slug'
        
        
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'job', 'user', 'created_at')
        read_only_fields = ('created_at',)


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    bookmark = BookmarkSerializer(required=False, read_only=True)
    get_user = serializers.CharField(source='user', required=False, read_only=True)
    get_company = serializers.CharField(source='company', required=False, read_only=True)
    get_location = serializers.CharField(source='location', required=False, read_only=True)
    get_category = serializers.CharField(source='category', required=False, read_only=True)
    applicants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    timesince = serializers.SerializerMethodField(required=False, read_only=True)
    get_job_type = serializers.CharField(source='job_type', required=False, read_only=True)
    get_created_at = serializers.DateTimeField(source='created_at', required=False, read_only=True)
    days_left = serializers.SerializerMethodField(required=False, read_only=True)
    plan_title = serializers.ReadOnlyField(source='plan.title')
    views_count = serializers.IntegerField(read_only=True)
    click_count = serializers.IntegerField(read_only=True)
    truncated_description = serializers.CharField(read_only=True)

    def get_timesince(self, obj):
        return obj.timesince()

    def get_days_left(self, obj):
        return obj.days_left()

    class Meta:
        model = Job
        fields = (
            'title', 'slug', 'truncated_description', 'description', 'view_count', 'click_count', 'get_user', 'get_company', 'get_location', 'user',
            'get_category', 'company', 'location',  'address', 'category', 'job_type', 'work_experience', 'education_level', 'min_salary', 'max_salary', 'currency', 'salary_type',
            'created_at', 'updated_at', 'is_active', 'applicants', 'timesince', 'get_job_type',
            'get_created_at', 'days_left', 'plan_title', 'views_count', 'click_count', 'bookmarks', 'bookmark'
        )
        read_only_fields = ('created_at', 'updated_at', 'is_active', 'slug')

    def create(self, validated_data):
        return super().create(validated_data)



class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('id', 'job', 'user', 'resume', 'cover_letter', 'is_active', 'created_at')
        read_only_fields = ('created_at', 'is_active')


class ImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impression
        fields = ('id', 'job', 'source_ip', 'session_id', 'created_at')
        read_only_fields = ('created_at',)


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ('id', 'job', 'source_ip', 'session_id', 'created_at')
        read_only_fields = ('created_at',)
