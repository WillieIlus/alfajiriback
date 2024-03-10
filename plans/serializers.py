from rest_framework import serializers

from .models import Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_active', 'is_default', 'is_fallback')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price_per_day'] = float(data['price_per_day'])
        return data
