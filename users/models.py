from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.CharField(max_length=100)



class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login = models.BooleanField()  # True for login, False for logout
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        login_type = 'login' if self.login else 'logout'
        return f"{self.user.username} - {login_type} at {self.timestamp}"
