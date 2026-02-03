from django.db import models
from django.utils import timezone


class SystemMetric(models.Model):
    """Model to store system performance metrics."""
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    
    # CPU metrics
    cpu_percent = models.FloatField(help_text="CPU usage percentage")
    
    # Memory metrics
    memory_total = models.BigIntegerField(help_text="Total memory in bytes")
    memory_available = models.BigIntegerField(help_text="Available memory in bytes")
    memory_used = models.BigIntegerField(help_text="Used memory in bytes")
    memory_percent = models.FloatField(help_text="Memory usage percentage")
    
    # Disk metrics (stored as JSON for multiple drives/partitions)
    disk_usage = models.JSONField(help_text="Disk usage per partition/drive")
    
    # Network metrics
    network_sent = models.BigIntegerField(help_text="Bytes sent", default=0)
    network_recv = models.BigIntegerField(help_text="Bytes received", default=0)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"Metric at {self.timestamp} - CPU: {self.cpu_percent}%, Memory: {self.memory_percent}%"
