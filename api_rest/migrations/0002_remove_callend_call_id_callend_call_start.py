# Generated by Django 5.1.2 on 2024-11-04 23:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callend',
            name='call_id',
        ),
        migrations.AddField(
            model_name='callend',
            name='call_start',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='api_rest.callstart', to_field='call_id'),
        ),
    ]
