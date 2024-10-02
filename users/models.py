from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    """
    Represents a user's profile information, including a profile photo.
    
    The `Profile` model is linked to a `User` instance via a one-to-one relationship. 
    This allows each user to have their own profile-specific data, such as a profile photo, stored 
    separately from the core user account information.
"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.CharField(max_length=100)



class UserLog(models.Model):
    """
        Represents a log of a user's login and logout events.
    
        The `UserLog` model tracks when a user logs in and out of the system. Each log entry
        contains the user who performed the action, whether it was a login or logout, and the
        timestamp of the event.
"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login = models.BooleanField()  # True for login, False for logout
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        login_type = 'login' if self.login else 'logout'
        return f"{self.user.username} - {login_type} at {self.timestamp}"
