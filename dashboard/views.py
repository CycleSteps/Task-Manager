from django.shortcuts import render,redirect
from task_manager.models import Project
from reports.models import ProjectInfo
from task_manager.models import Project
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
            return redirect('signIn')

    user = request.user
    projects = Project.objects.all()
    list = []

    for p in projects:
        if p.owner == user or user.id in p.get_members():
            list.append(ProjectInfo(p))

    data = {"user": user,
            "first": user.username[0],
            "other_users": User.objects.filter(~Q(id=user.id)).all(),
            "projects": list,
            }
    return render(request,"dashboard.html",data)