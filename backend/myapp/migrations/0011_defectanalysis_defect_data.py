# Generated by Django 5.1.4 on 2025-03-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_defectanalysis_is_watertight'),
    ]

    operations = [
        migrations.AddField(
            model_name='defectanalysis',
            name='defect_data',
            field=models.JSONField(default=dict),
        ),
    ]
