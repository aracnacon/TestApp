from django.contrib import admin
from .models import SystemMetric


@admin.register(SystemMetric)
class SystemMetricAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'cpu_percent', 'memory_percent', 'network_sent', 'network_recv']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
