import datetime
import json
import random
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST
from reports.models import ProjectInfo
from .models import Task, Project,Subtask, Comment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response



class Projects(View):
    def get(self, request):
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
        return render(request, 'projects.html', data)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('signIn')

        name = request.POST['name']
        description = request.POST['desc']
        details = request.POST['details']
        owner = request.user
        user_ids = request.POST.getlist('users', [])

        ids = []
        for id in user_ids:
            ids.append(int(id))

        n = random.randint(1, 7)
        pf_url = f'/media/project-logos/{n}.png'

        proj = Project.objects.create(name=name, description=description, details=details, owner=owner,
                                      members=json.dumps(ids), profile_photo=pf_url)
        proj.save()

        return redirect('boards')


class MangeProject(View):
    def post(self, request, id):
        Project.objects.filter(id=id).delete()

        response = JsonResponse({"message": "OK"})
        response.status_code = 200
        return response


# @method_decorator(csrf_exempt, name='dispatch')
class Tasks(View):
    http_method_names = ['get', 'post', 'put']  # Add PUT to allowed methods

    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect("signIn")

        proj = Project.objects.filter(id=id).first()
        user = request.user
        users = User.objects.filter(Q(id__in=proj.get_members()) | Q(id=proj.owner.id))
        data = {
            "user": user,
            "first": user.username[0],
            "other_users": users,
            "tasks": proj.task_set.all(),
            'proj': proj,
            "can_add": user == proj.owner
        }
        return render(request, 'tasks.html', data)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return redirect('signIn')

        name = request.POST['name']
        description = request.POST['desc']
        assigned_users = request.POST.getlist('users')  # This will get a list of selected user IDs
        status = 'T'
        end_time = request.POST['date']

        # Create the task
        task = Task(name=name, description=description, status=status, end_time=end_time, project_id=id)
        
        # Save the task first to generate the ID
        task.save()

        # Associate selected users with the task
        for user_id in assigned_users:
            user = User.objects.get(id=user_id)  # Fetch user instance
            task.assigned_to.add(user)  # Add user to the ManyToManyField

        return redirect('tasks', id=id)

    def put(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        # Parse the JSON body from the PUT request
        body = json.loads(request.body.decode('utf-8'))

        task_id = body.get('task_id')
        name = body.get('name')
        description = body.get('description')

        task = Task.objects.filter(id=task_id, project_id=id).first()

        if task:
            task.name = name
            task.description = description

            task.save()
            return render(request, 'tasks.html')
        else:
           return render(request, 'tasks.html')

@api_view(['POST'])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_title = request.data.get('name')
    new_description = request.data.get('description')

    if new_title:
        task.name = new_title
    if new_description:
        task.description = new_description

    task.save()

    return Response({
        'success': True,
        'message': 'Task updated successfully',
        'name': task.name,
        'description': task.description,
    })
    
    
class ManegeTasks(View):
    def post(self, request, id):
        if not request.user.is_authenticated:
            response = JsonResponse({"error": "Invalid User"})
            response.status_code = 403
            return response

        user = request.user

        type = request.POST['type']
        if type == 'edit_status':
            task_id = request.POST['task_id']
            status = request.POST['board_id']

            task = Task.objects.filter(id=task_id).first()

            if status in ['O', 'B', 'L'] or task.status in ['O', 'B', 'L']:
                if user == task.project.owner:
                    task.status = status
                    task.save()

                else:
                    response = JsonResponse({"error": "You Do Not Have Permission"})
                    response.status_code = 403
                    return response
            else:
                if user == task.assigned_to or user == task.project.owner:
                    task.status = status
                    if status == 'D':
                        task.start_time = datetime.datetime.today().date()
                    task.save()
                else:
                    response = JsonResponse({"error": "You Do Not Have Permission"})
                    response.status_code = 403
                    return response

            response = JsonResponse({"message": "OK"})
            response.status_code = 200
            return response

        if type == 'edit_end_time':

            task_id = request.POST['task_id']
            end_time = request.POST['new_end_time']

            task = Task.objects.filter(id=task_id).first()

            if user == task.project.owner:
                task.end_time = end_time
                task.save()

                response = JsonResponse({"message": "OK"})
                response.status_code = 200
                return response

            else:
                response = JsonResponse({"error": "You Do Not Have Permission"})
                response.status_code = 403
                return response



@method_decorator(login_required, name='dispatch')
class UpdateSubtaskStatusView(View):
    def post(self, request):
        data = json.loads(request.body)
        subtask_id = data.get('subtask_id')
        is_completed = data.get('is_completed')

        try:
            subtask = Subtask.objects.get(id=subtask_id)
            subtask.is_completed = is_completed
            subtask.save()

            # Optionally, calculate the completion percentage
            task = subtask.task
            total_subtasks = task.subtasks.count()
            completed_subtasks = task.subtasks.filter(is_completed=True).count()
            progress_percentage = (completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0


            # Update the task with the new progress percentage if necessary
            task = subtask.task  # Assuming your Subtask has a ForeignKey to Task
            self.update_task_progress(task)

            return JsonResponse({
                'status': 'success',
                'progress': progress_percentage,
                'task_id': task.id
            })

        except Subtask.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Subtask not found'}, status=404)
        
    def update_task_progress(self, task):
        subtasks = task.subtasks.all()
        total_subtasks = subtasks.count()
        completed_subtasks = subtasks.filter(is_completed=True).count()
        progress = (completed_subtasks / total_subtasks) * 100 if total_subtasks > 0 else 0
        task.progress = progress
        task.save()



@method_decorator(csrf_exempt, name='dispatch')
class AddCommentView(View):
    @method_decorator(login_required)  # Apply the login_required decorator here
    def post(self, request):
        data = json.loads(request.body)
        task_id = data.get('task_id')
        text = data.get('text')
        
        try:
            task = Task.objects.get(id=task_id)
            comment = Comment.objects.create(task=task, user=request.user, text=text)

            return JsonResponse({'status': 'success', 'username': request.user.username, 'text': comment.text})

        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
        

@method_decorator(csrf_exempt, name='dispatch')
class AddSubtaskView(View):
    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        task_id = data.get('task_id')
        description = data.get('description')

        try:
            task = Task.objects.get(id=task_id)
            subtask = Subtask.objects.create(task=task, description=description)

            return JsonResponse({'status': 'success', 'subtask_id': subtask.id, 'description': subtask.description})

        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)