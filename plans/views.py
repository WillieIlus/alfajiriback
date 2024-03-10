from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Plan
from .serializers import PlanSerializer

class PlanListCreateAPIView(ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class PlanRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'plan_id'
