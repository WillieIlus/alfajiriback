from django.contrib import admin

from .models import Plan

class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_per_day', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

admin.site.register(Plan, PlanAdmin)
