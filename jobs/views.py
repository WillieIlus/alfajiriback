import logging
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse, Http404
from rest_framework.views import APIView

from .models import Job, JobApplication, Impression, Click, Bookmark
from .serializers import JobSerializer, JobApplicationSerializer, ImpressionSerializer, ClickSerializer, BookmarkSerializer
from .filters import JobFilter

from accounts.models import User
from accounts.serializers import UserSerializer
from companies.models import Company
from companies.serializers import CompanySerializer
from locations.models import Location
from locations.serializers import LocationSerializer
from categories.models import Category
from categories.serializers import CategorySerializer

class JobViewSet(ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        current_time = timezone.now()
        time_since_last_viewed = current_time - timedelta(minutes=75)
        for job in queryset:
            if job.last_viewed_at and job.last_viewed_at > time_since_last_viewed:
                job.view_count += 1
                job.save(update_fields=['view_count'])
            else:
                pass
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CompanyJobViewSet(ListAPIView):
    serializer_class = JobSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def get_queryset(self):
        company = Company.objects.get(slug=self.kwargs['slug'])
        return Job.objects.filter(company=company)


class LocationJobViewSet(ListAPIView):
    serializer_class = JobSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def get_queryset(self):
        location = Location.objects.get(slug=self.kwargs['slug'])
        return Job.objects.filter(location=location)


class CategoryJobViewSet(ListAPIView):
    serializer_class = JobSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return Job.objects.filter(category=category)


class UserJobViewSet(ListAPIView):
    serializer_class = JobSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def get_queryset(self):
        user = User.objects.get(user=self.kwargs['user'])
        return Job.objects.filter(user=user)


class JobDetailsViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        time_since_last_clicked = timezone.now() - timedelta(minutes=75)

        # Check if last_clicked_at is not None and greater than time_since_last_clicked
        if instance.last_clicked_at and instance.last_clicked_at > time_since_last_clicked:
            instance.click_count += 1
            instance.view_count += 1
            instance.save(update_fields=['click_count', 'view_count'])
            instance.update_last_viewed()
            instance.update_last_clicked()

        # Always increment view_count by 1
        else:
            instance.view_count += 1
            instance.save(update_fields=['view_count'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class JobApplicationViewSet(ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        job = Job.objects.get(slug=self.kwargs['slug'])
        serializer.save(user=self.request.user, job=job)


class JobApplicationDetailsViewSet(RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'


class ImpressionViewSet(ListCreateAPIView):
    queryset = Impression.objects.all()
    serializer_class = ImpressionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        job = Job.objects.get(slug=self.kwargs['slug'])
        source_ip = self.request.META.get('REMOTE_ADDR')

        # Increment impression count only if there's no impression from the same IP in the last 30 minutes
        if not Impression.objects.filter(
                job=job, source_ip=source_ip, created_at__gte=timezone.now() - timedelta(minutes=30)
        ).exists():
            job.impression_count += 1
            job.save(update_fields=['impression_count'])
            job.update_last_impression()

        serializer.save(job=job, source_ip=source_ip)


class BookmarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        job = Job.objects.get(slug=self.kwargs['slug'])
        serializer.save(user=self.request.user, job=job)

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'message': 'Bookmark deleted successfully'}, status=204)

    def perform_destroy(self, instance):
        instance.delete()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookmarkSerializer
        return BookmarkSerializer

    def get_serializer(self, *args, **kwargs):

        if self.request.method == 'GET':
            kwargs['context'] = self.get_serializer_context()
            return BookmarkSerializer(*args, **kwargs)
        return BookmarkSerializer(*args, **kwargs)

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return BookmarkSerializer
        return BookmarkSerializer

    def get_serializer(self, *args, **kwargs):

        if self.request.method == 'GET':
            kwargs['context'] = self.get_serializer_context()
            return BookmarkSerializer(*args, **kwargs)
        return BookmarkSerializer(*args, **kwargs)
