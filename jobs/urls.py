from django.urls import path
from .views import JobViewSet, JobDetailsViewSet, apply_for_job, ToggleBookmarkView, UserBookmarksView

app_name = 'jobs'

urlpatterns = [
    path('bookmarks/', UserBookmarksView.as_view(), name='user_bookmarks'),
    path('', JobViewSet.as_view(), name='jobs'),
    path('<slug:slug>/', JobDetailsViewSet.as_view(), name='details'),
    path('apply/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('<int:job_id>/bookmark/', ToggleBookmarkView.as_view(), name='toggle_bookmark'),
]