from django.urls import path
from .views import JobViewSet, JobDetailsViewSet, ToggleBookmarkView, UserBookmarksView, JobApplicationView

app_name = 'jobs'

urlpatterns = [
    path('bookmarks/', UserBookmarksView.as_view(), name='user_bookmarks'),
    path('', JobViewSet.as_view(), name='jobs'),
    path('<slug:slug>/', JobDetailsViewSet.as_view(), name='details'),
    path('apply/<int:job_id>/', JobApplicationView.as_view(), name='apply-for-job'),
    path('<int:job_id>/bookmark/', ToggleBookmarkView.as_view(), name='toggle_bookmark'),
]
