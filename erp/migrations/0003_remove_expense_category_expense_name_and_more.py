# Generated by Django 5.1.6 on 2025-02-26 19:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='category',
        ),
        migrations.AddField(
            model_name='expense',
            name='name',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
