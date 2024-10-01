from django.contrib import admin
from users.models import Profile,UserLog

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_photo')
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)

# admin.py

from django.contrib import admin
from .models import UserLog

@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'login', 'timestamp')
    list_filter = ('login', 'timestamp')
