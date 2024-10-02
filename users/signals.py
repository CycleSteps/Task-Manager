# signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from users.models import UserLog


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
Logs user login and logout events in the UserLog model.

The `log_user_login` function is called when a user logs in, and creates a new UserLog
instance with the `login` field set to `True`.

The `log_user_logout` function is called when a user logs out, and creates a new UserLog
instance with the `login` field set to `False`.
"""
    UserLog.objects.create(user=user, login=True)  # True for login

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, login=False)  # False for logout
