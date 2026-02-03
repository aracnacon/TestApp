from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Max, Min
from .models import SystemMetric
from .serializers import SystemMetricSerializer
from .collectors import collect_system_metrics


class SystemMetricViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and collecting system metrics."""
    queryset = SystemMetric.objects.all()
    serializer_class = SystemMetricSerializer
    
    def get_queryset(self):
        """Optionally filter by time range."""
        queryset = SystemMetric.objects.all()
        
        # Filter by time range if provided
        hours = self.request.query_params.get('hours', None)
        if hours:
            try:
                hours = int(hours)
                since = timezone.now() - timedelta(hours=hours)
                queryset = queryset.filter(timestamp__gte=since)
            except ValueError:
                pass
        
        return queryset.order_by('-timestamp')
    
    @action(detail=False, methods=['post'])
    def collect(self, request):
        """Collect and store current system metrics."""
        try:
            metrics_data = collect_system_metrics()
            serializer = self.get_serializer(data=metrics_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the most recent system metrics."""
        latest = SystemMetric.objects.first()
        if latest:
            serializer = self.get_serializer(latest)
            return Response(serializer.data)
        return Response(
            {'message': 'No metrics available'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get aggregated statistics for metrics."""
        hours = request.query_params.get('hours', 24)
        try:
            hours = int(hours)
        except ValueError:
            hours = 24
        
        since = timezone.now() - timedelta(hours=hours)
        queryset = SystemMetric.objects.filter(timestamp__gte=since)
        
        if not queryset.exists():
            return Response(
                {'message': 'No metrics available for the specified time range'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        stats = queryset.aggregate(
            avg_cpu=Avg('cpu_percent'),
            max_cpu=Max('cpu_percent'),
            min_cpu=Min('cpu_percent'),
            avg_memory=Avg('memory_percent'),
            max_memory=Max('memory_percent'),
            min_memory=Min('memory_percent'),
        )
        
        return Response({
            'time_range_hours': hours,
            'total_samples': queryset.count(),
            'cpu': {
                'average': round(stats['avg_cpu'] or 0, 2),
                'maximum': round(stats['max_cpu'] or 0, 2),
                'minimum': round(stats['min_cpu'] or 0, 2),
            },
            'memory': {
                'average': round(stats['avg_memory'] or 0, 2),
                'maximum': round(stats['max_memory'] or 0, 2),
                'minimum': round(stats['min_memory'] or 0, 2),
            },
        })
