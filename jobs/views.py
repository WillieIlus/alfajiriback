import logging
from rest_framework import status, viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Job, JobApplication, Impression, Bookmark
from .serializers import JobSerializer, JobApplicationSerializer, ImpressionSerializer, BookmarkSerializer
from .filters import JobFilter

logger = logging.getLogger(__name__)


class JobViewSet(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        current_time = timezone.now()
        time_since_last_viewed = current_time - timedelta(minutes=37)

        for job in queryset:
            if job.last_viewed_at and job.last_viewed_at > time_since_last_viewed:
                job.view_count += 1
                job.save(update_fields=['view_count'])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JobDetailsViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        time_since_last_clicked = timezone.now() - timedelta(minutes=75)

        if instance.last_clicked_at and instance.last_clicked_at > time_since_last_clicked:
            instance.click_count += 1

        instance.view_count += 1
        instance.save(update_fields=['click_count', 'view_count'])
        instance.update_last_viewed()
        instance.update_last_clicked()

        serializer = self.get_serializer(instance)
        data = serializer.data

        # Add related jobs to the response
        related_jobs = Job.objects.filter(
            Q(category=instance.category) | Q(company=instance.company)
        ).exclude(id=instance.id).order_by('-created_at')[:3]

        related_serializer = self.get_serializer(related_jobs, many=True)
        data['related_jobs'] = related_serializer.data

        return Response(data)


class CompanyJobViewSet(generics.ListAPIView):
    serializer_class = JobSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def get_queryset(self):
        return Job.objects.filter(company__slug=self.kwargs['slug'])


class JobApplicationView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job_id = self.kwargs.get('job_id')
        job = Job.objects.get(id=job_id)
        serializer.save(
            user=self.request.user,
            employer_email=job.email,
            job=job
        )

class ToggleBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        bookmark, created = Bookmark.objects.get_or_create(job=job, user=request.user)

        if created:
            job.bookmarks += 1
            job.save()
            return Response({'status': 'Bookmark added'}, status=status.HTTP_201_CREATED)
        else:
            bookmark.delete()
            job.bookmarks -= 1
            job.save()
            return Response({'status': 'Bookmark removed'}, status=status.HTTP_200_OK)

class UserBookmarksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)


class ImpressionViewSet(generics.ListCreateAPIView):
    queryset = Impression.objects.all()
    serializer_class = ImpressionSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        job = Job.objects.get(slug=self.kwargs['slug'])
        source_ip = self.request.META.get('REMOTE_ADDR')

        if not Impression.objects.filter(
                job=job, source_ip=source_ip, created_at__gte=timezone.now() - timedelta(minutes=30)
        ).exists():
            job.impression_count += 1
            job.save(update_fields=['impression_count'])
            job.update_last_impression()

        serializer.save(job=job, source_ip=source_ip)