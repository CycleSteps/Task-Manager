from django.contrib import admin
from users.models import Profile,UserLog


class ProfileAdmin(admin.ModelAdmin):
    """
    The `ProfileAdmin` class is a Django admin model that provides a customized interface for managing `Profile` objects
      in the Django admin site.
    
    The `list_display` attribute specifies the fields that should be displayed in the admin list view for `Profile` objects. 
    In this case, the `user` and `profile_photo` fields are displayed.
    
    The `search_fields` attribute specifies the fields that should be used to search for `Profile` objects in the admin interface. 
    In this case, the `user__username` field can be used to search for profiles.
    """
    list_display = ('user', 'profile_photo')
    search_fields = ('user__username',)

admin.site.register(Profile, ProfileAdmin)

# admin.py

from django.contrib import admin
from .models import UserLog



@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    """
The `UserLogAdmin` class is a Django admin model that provides a customized interface for managing `UserLog` objects in the Django admin site.

The `list_display` attribute specifies the fields that should be displayed in the admin list view for `UserLog` objects. 
In this case, the `user`, `login`, and `timestamp` fields are displayed.

The `list_filter` attribute specifies the fields that should be used to filter the list of `UserLog` objects in the admin interface.
In this case, the `login` and `timestamp` fields can be used to filter the list.
"""
    list_display = ('user', 'login', 'timestamp')
    list_filter = ('login', 'timestamp')
