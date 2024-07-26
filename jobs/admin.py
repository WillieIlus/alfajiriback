from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from django.db import models
from .models import Job, JobApplication, Impression, Click, Bookmark
from .resource import JobResource
from import_export.admin import ImportExportModelAdmin


class JobAdmin(ImportExportModelAdmin):
    resource_class = JobResource
    list_display = ('title', 'view_count', 'click_count', 'slug', 'category', 'company', 'location', 'is_active')
    prepopulated_fields = {'slug': ('title', 'company')}
    list_filter = ('category', 'company', 'location', 'is_active')
    search_fields = ('title', 'description', 'requirements', 'company__name', 'location__name')
    list_per_page = 20


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'is_active')
    list_filter = ('job', 'user', 'is_active')
    search_fields = ('job__title', 'user__username')
    list_per_page = 20


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('job', 'source_ip', 'session_id', 'created_at')
    list_filter = ('job', 'source_ip', 'session_id')
    search_fields = ('job__title', 'source_ip', 'session_id')
    list_per_page = 20


class ClickAdmin(admin.ModelAdmin):
    list_display = ('job', 'source_ip', 'session_id', 'created_at')
    list_filter = ('job', 'source_ip', 'session_id')
    search_fields = ('job__title', 'source_ip', 'session_id')
    list_per_page = 20


admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(Impression, ImpressionAdmin)
admin.site.register(Click, ClickAdmin)
admin.site.register(Bookmark)
