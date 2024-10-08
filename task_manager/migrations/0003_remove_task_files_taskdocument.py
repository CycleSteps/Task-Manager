# Generated by Django 5.1.1 on 2024-09-25 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_task_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='files',
        ),
        migrations.CreateModel(
            name='TaskDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='task_files/')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='task_manager.task')),
            ],
        ),
    ]
