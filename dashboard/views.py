from django.shortcuts import render,redirect
from task_manager.models import Project,Task
from reports.models import ProjectInfo
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

    user = request.user
    
    # Count of projects owned by the user
    my_projects_count = Project.objects.filter(owner=user).count()
    
    # Count of tasks owned by the user
    my_tasks_count = Task.objects.filter(project__owner=user).count()
    
    # Count of projects assigned to the user
    projects_assigned_count = Project.objects.filter(members__contains=user.id).count()
    
    # Count of tasks assigned to the user
    tasks_assigned_count = Task.objects.filter(assigned_to=user).count()

    context = {
        'my_projects_count': my_projects_count,
        'my_tasks_count': my_tasks_count,
        'projects_assigned_count': projects_assigned_count,
        'tasks_assigned_count': tasks_assigned_count,
        "user": user,
        "first": user.username[0],
        "other_users": User.objects.filter(~Q(id=user.id)).all(),
        "projects": list,
    }

    return render(request, 'dashboard.html', context)