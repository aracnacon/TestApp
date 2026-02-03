# Generated migration for SystemMetric model

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('cpu_percent', models.FloatField(help_text='CPU usage percentage')),
                ('memory_total', models.BigIntegerField(help_text='Total memory in bytes')),
                ('memory_available', models.BigIntegerField(help_text='Available memory in bytes')),
                ('memory_used', models.BigIntegerField(help_text='Used memory in bytes')),
                ('memory_percent', models.FloatField(help_text='Memory usage percentage')),
                ('disk_usage', models.JSONField(help_text='Disk usage per partition/drive')),
                ('network_sent', models.BigIntegerField(default=0, help_text='Bytes sent')),
                ('network_recv', models.BigIntegerField(default=0, help_text='Bytes received')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='systemmetric',
            index=models.Index(fields=['-timestamp'], name='metrics_sys_timesta_idx'),
        ),
    ]
