"""
Cross-platform system metrics collector using psutil.
Supports Windows, macOS, and Linux.
"""
import psutil
import platform
from datetime import datetime


def collect_system_metrics():
    """
    Collect current system metrics from the host.
    Returns a dictionary with all metric data.
    """
    try:
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics - collect for all partitions/drives
        disk_usage = {}
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            try:
                # Skip CD-ROM drives and other non-filesystem mounts
                if partition.fstype:
                    usage = psutil.disk_usage(partition.mountpoint)
                    # Use device/mountpoint as key (handles Windows C:, D: etc.)
                    disk_usage[partition.device] = {
                        'mountpoint': partition.mountpoint,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent,
                        'fstype': partition.fstype,
                    }
            except (PermissionError, OSError):
                # Skip partitions we can't access
                continue
        
        # Network metrics - sum all interfaces
        network_io = psutil.net_io_counters()
        network_sent = network_io.bytes_sent if network_io else 0
        network_recv = network_io.bytes_recv if network_io else 0
        
        return {
            'timestamp': datetime.now(),
            'cpu_percent': round(cpu_percent, 2),
            'memory_total': memory.total,
            'memory_available': memory.available,
            'memory_used': memory.used,
            'memory_percent': round(memory.percent, 2),
            'disk_usage': disk_usage,
            'network_sent': network_sent,
            'network_recv': network_recv,
        }
    except Exception as e:
        raise Exception(f"Error collecting system metrics: {str(e)}")


def get_system_info():
    """Get basic system information."""
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
    }
