from django.urls import path
from .views import JobViewSet, CompanyJobViewSet, LocationJobViewSet, CategoryJobViewSet, UserJobViewSet, BookmarkViewSet, JobApplicationViewSet, JobDetailsViewSet

app_name = 'jobs'

urlpatterns = [
    path('', JobViewSet.as_view(), name='jobs'),
    path('<slug:slug>/', JobDetailsViewSet.as_view(), name='details'),
    # path('<slug:slug>/related/', JobDetailsViewSet.as_view({'get': 'related'}), name='job-related'),
    path('company/<slug:slug>/', CompanyJobViewSet.as_view(), name='company-jobs'),
    path('location/<slug:slug>/', LocationJobViewSet.as_view(), name='location-jobs'),
    path('category/<slug:slug>/', CategoryJobViewSet.as_view(), name='category-jobs'),
    path('user/<slug:slug>/', UserJobViewSet.as_view(), name='user-jobs'),
    path('bookmark/', BookmarkViewSet.as_view({'post': 'create', 'delete': 'destroy', 'get': 'list'}), name='bookmark'),
    path('apply/', JobApplicationViewSet.as_view(), name='apply'),
    path('apply/<slug:slug>/', JobApplicationViewSet.as_view(), name='apply'),
]
