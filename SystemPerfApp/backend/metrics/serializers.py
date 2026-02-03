from rest_framework import serializers
from .models import SystemMetric


class SystemMetricSerializer(serializers.ModelSerializer):
    """Serializer for SystemMetric model."""
    
    class Meta:
        model = SystemMetric
        fields = [
            'id',
            'timestamp',
            'cpu_percent',
            'memory_total',
            'memory_available',
            'memory_used',
            'memory_percent',
            'disk_usage',
            'network_sent',
            'network_recv',
        ]
        read_only_fields = ['id', 'timestamp']
