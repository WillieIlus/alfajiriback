from django.urls import path

from .views import PlanListCreateAPIView, PlanRetrieveUpdateDestroyAPIView

app_name = 'plans'

urlpatterns = [
    path('', PlanListCreateAPIView.as_view(), name='list_create'),
    path('<int:plan_id>/', PlanRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy'),
]
