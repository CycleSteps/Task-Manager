from django.apps import AppConfig
from django.contrib import admin

class CustomAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customadmin'

    def ready(self):
        admin.site.site_header = "Task Manager"
        admin.site.site_title = "Task Manager"
        admin.site.index_title = "Task Manager"
