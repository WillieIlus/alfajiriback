from .models import Job
from locations.models import Location
from categories.models import Category
from companies.models import Company
from django_filters import rest_framework as filters


class JobFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    location = filters.ModelChoiceFilter(queryset=Location.objects.all())
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    company = filters.ModelChoiceFilter(queryset=Company.objects.all()) #added
    min_salary = filters.NumberFilter(field_name='min_salary', lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name='max_salary', lookup_expr='lte')
    job_type = filters.ChoiceFilter(choices=Job.JOB_TYPE_CHOICES)
    vacancies = filters.NumberFilter(field_name='vacancies', lookup_expr='gte')

    class Meta:
        model = Job
        fields = {
            'title',
            'location',
            'category',
            'company',
            'min_salary',
            'max_salary',
            'job_type',
            'vacancies'
        }



# from django_filters import rest_framework as filters
# from .models import Job
# from locations.models import Location
# from categories.models import Category
# from companies.models import Company
#
# class JobFilter(filters.FilterSet):
#     title = filters.CharFilter(lookup_expr='icontains')
#     location = filters.ModelChoiceFilter(queryset=Location.objects.all(), required=False)
#     category = filters.ModelChoiceFilter(queryset=Category.objects.all(), required=False)
#     company = filters.ModelChoiceFilter(queryset=Company.objects.all(), required=False)
#     min_salary = filters.NumberFilter(field_name='min_salary', lookup_expr='gte', required=False)
#     max_salary = filters.NumberFilter(field_name='max_salary', lookup_expr='lte', required=False)
#     job_type = filters.ChoiceFilter(choices=Job.JOB_TYPE_CHOICES, required=False)
#     vacancies = filters.NumberFilter(field_name='vacancies', lookup_expr='gte', required=False)
#
#     class Meta:
#         model = Job
#         fields = ['title', 'location', 'category', 'company', 'min_salary', 'max_salary', 'job_type', 'vacancies']
#
#     def filter_queryset(self, queryset):
#         for name, value in self.form.cleaned_data.items():
#             if value is not None and value != '':
#                 queryset = self.filters[name].filter(queryset, value)
#         return queryset
#
#