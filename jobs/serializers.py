from rest_framework import serializers

from .models import Job, JobApplication, Impression, Click, Bookmark
from accounts.models import User
from companies.models import Company
from locations.models import Location
from categories.models import Category
from django.utils.text import slugify
from django.db import IntegrityError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'phone'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = 'id', 'name', 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name', 'slug'


class CompanySerializer(serializers.ModelSerializer):
    get_user = serializers.CharField(source='user', required=False)
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Company
        fields = 'id', 'name', 'slug', 'logo', 'website', 'description', 'get_user',


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    get_user = serializers.CharField(source='user', required=False, read_only=True)
    get_company = CompanySerializer(source='company', read_only=True)
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
    apply_count = serializers.IntegerField(read_only=True)
    truncated_description = serializers.CharField(read_only=True)

    image = serializers.ImageField(required=False, allow_null=True)

    def get_timesince(self, obj):
        return obj.timesince()

    def get_days_left(self, obj):
        return obj.days_left()

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'slug', 'truncated_description', 'description', 'view_count', 'click_count', 'apply_count',
            'get_user', 'get_company', 'get_location', 'user', 'email', 'image', 'vacancies', 'work_hours',
            'work_hour_type', 'deadline', 'application_contact',
            'get_category', 'company', 'location', 'address', 'category', 'job_type', 'work_experience',
            'education_level', 'min_salary', 'max_salary', 'currency', 'salary_type',
            'created_at', 'updated_at', 'is_active', 'applicants', 'timesince', 'get_job_type',
            'get_created_at', 'days_left', 'plan_title', 'views_count', 'click_count', 'bookmarks'
        )
        read_only_fields = (
        'created_at', 'updated_at', 'is_active', 'slug', 'truncated_description', 'view_count', 'click_count',
        'apply_count', 'get_user', 'get_company', 'get_location', 'user', 'get_category', 'applicants', 'timesince',
        'get_job_type', 'get_created_at', 'days_left', 'plan_title', 'views_count', 'click_count')

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle file updates
        image = validated_data.pop('image', None)
        if image is not None:
            instance.image = image

        # Get the new title if it exists
        new_title = validated_data.get('title', instance.title)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Only update the slug if the title has changed
        if new_title != instance.title:
            self._update_slug(instance, new_title)

        instance.save()
        return instance

    def _update_slug(self, instance, new_title):
        """Update the slug only if necessary."""
        new_slug = slugify(new_title)
        if new_slug != instance.slug:
            if not Job.objects.filter(slug=new_slug).exclude(pk=instance.pk).exists():
                instance.slug = new_slug
            else:
                self._generate_unique_slug(instance, new_title)

    def _generate_unique_slug(self, instance, title):
        """Generate a unique slug for the instance."""
        base_slug = slugify(title)
        unique_slug = base_slug
        num = 1
        while Job.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        instance.slug = unique_slug
        

class BookmarkSerializer(serializers.ModelSerializer):
    job = JobSerializer()

    class Meta:
        model = Bookmark
        fields = ('id', 'job', 'user', 'is_active', 'created_at')
        read_only_fields = ('created_at',)


class JobApplicationSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'employer_email', 'user', 'resume', 'cover_letter', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_active', 'created_at', 'user', 'employer_email']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle file updates
        resume = validated_data.pop('resume', None)
        if resume is not None:
            instance.resume = resume

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
