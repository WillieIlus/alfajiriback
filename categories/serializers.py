from  rest_framework import serializers

from jobs.models import Job
from jobs.serializers import JobSerializer
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    total_jobs = serializers.SerializerMethodField()
    jobs = JobSerializer(many=True, read_only=True)

    def get_total_jobs (self, category):
        return Job.objects.filter(category=category).count()

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['slug']

