from django.db import models
from django.contrib.auth.models import User
import json


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    details = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.CharField(max_length=500)
    profile_photo = models.CharField(max_length=200, default='/static/media/project-logos/1.png')

    def get_members(self):
        return json.loads(self.members)


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    assigned_to = models.ManyToManyField(User)
    status_choices = (
        ('T', 'To Do'),
        ('D', 'Doing'),
        ('I', 'In Test'),
        ('O', 'Done'),
        ('B', 'Blocked'),
        ('L', 'Deleted')
    )
    status = models.CharField(max_length=1, choices=status_choices)
    start_time = models.DateField(null=True)
    end_time = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # Can be between 0.0 and 100.0



class Subtask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()