from django.urls import path
from .views import JobViewSet, JobDetailsViewSet, apply_for_job, bookmark_job, unbookmark_job

app_name = 'jobs'

urlpatterns = [
    path('', JobViewSet.as_view(), name='jobs'),
    path('<slug:slug>/', JobDetailsViewSet.as_view(), name='details'),
    path('apply/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('bookmark/<int:job_id>/', bookmark_job, name='bookmark_job'),
    path('unbookmark/<int:job_id>/', unbookmark_job, name='unbookmark_job'),
]