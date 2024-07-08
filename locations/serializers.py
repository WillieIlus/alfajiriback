from rest_framework import serializers
from .models import Country, Location

from jobs.models import Job
from jobs.serializers import JobSerializer

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'slug', 'code', 'flag')


class LocationSerializer(serializers.ModelSerializer):
    job_count = serializers.SerializerMethodField()
    jobs = JobSerializer(many=True, read_only=True)
    # country = CountrySerializer()

    def get_job_count(self, location):
        return Job.objects.filter(location=location).count()

    class Meta:
        model = Location
        fields = ('id', 'name', 'slug', 'country', 'flag', 'job_count', 'jobs')
        read_only_fields = ('country',)