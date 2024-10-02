from django.contrib import admin
from task_manager.models import Project, Task,Subtask, Comment,TaskDocument




class SubtaskInline(admin.TabularInline):
    """ The `SubtaskInline` class is a Django admin inline model that allows adding Subtask objects inline with a parent model, such as a Task. 
It has the following properties:

- `model`: Specifies the model class for the inline objects, which is Subtask in this case.
- `extra`: Specifies the number of empty forms to display for adding new Subtask objects, which is set to 1 in this case.

The `CommentInline` class is a Django admin inline model that allows adding Comment objects inline with a parent model, such as a Task. 
It has the following properties:

- `model`: Specifies the model class for the inline objects, which is Comment in this case.
- `extra`: Specifies the number of empty forms to display for adding new Comment objects, which is set to 1 in this case.

The `TaskDocumentInline` class is a Django admin inline model that allows adding TaskDocument objects inline with a parent model, such as a Task. 
It has the following properties:

- `model`: Specifies the model class for the inline objects, which is TaskDocument in this case.
- `extra`: Specifies the number of empty forms to display for adding new TaskDocument objects, which is set to 1 in this case. """
    model = Subtask
    extra = 1  # Number of empty forms to display

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty forms to display

# Inline class for TaskDocument in the TaskAdmin
class TaskDocumentInline(admin.TabularInline):
    model = TaskDocument
    extra = 1  # Allows adding extra documents in the admin interface


# Admin class for TaskDocument

@admin.register(TaskDocument)
class TaskDocumentAdmin(admin.ModelAdmin):
    """
The `TaskDocumentAdmin` class is a Django admin model for managing TaskDocument objects. It provides the following functionality:

- `list_display`: Specifies the fields to be displayed in the admin list view for TaskDocument objects. In this case, 
it displays the task, name, and file of each document.
- `search_fields`: Enables a search field in the admin interface to search for TaskDocument objects by their name or file.
- `list_filter`: Adds a filter sidebar in the admin interface to allow filtering TaskDocument objects by their task.

The `ProjectAdmin` class is a Django admin model for managing Project objects. It provides the following functionality:

- `list_display`: Specifies the fields to be displayed in the admin list view for Project objects. In this case, 
it displays the name, owner, and description of each project.
- `search_fields`: Enables a search field in the admin interface to search for Project objects by their name or description.
- `list_filter`: Adds a filter sidebar in the admin interface to allow filtering Project objects by their owner.

The `TaskAdmin` class is a Django admin model for managing Task objects. It provides the following functionality:

- `list_display`: Specifies the fields to be displayed in the admin list view for Task objects. In this case, 
it displays the name, project, status, start time, end time, and progress of each task.
- `search_fields`: Enables a search field in the admin interface to search for Task objects by their name or description.
- `list_filter`: Adds a filter sidebar in the admin interface to allow filtering Task objects by their status and assigned to.
"""
    list_display = ('task', 'name', 'file')
    search_fields = ('name', 'file')
    list_filter = ('task',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'description')  # Removed start_time and end_time
    search_fields = ('name', 'description')
    list_filter = ('owner',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'start_time', 'end_time','progress')  # Assuming these fields exist in Task
    search_fields = ('name', 'description')
    list_filter = ('status', 'assigned_to')




@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    """ The `SubtaskAdmin` class is a Django admin model for managing Subtask objects. It provides the following functionality:

- `list_display`: Specifies the fields to be displayed in the admin list view for Subtask objects. 
In this case, it displays the task, description, and completion status of each subtask.
- `list_filter`: Adds a filter sidebar in the admin interface to allow filtering Subtask objects by their completion status.
- `search_fields`: Enables a search field in the admin interface to search for Subtask objects by their description. """
    list_display = ('task', 'description', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('description',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ The `CommentAdmin` class is a Django admin model for managing Comment objects. It provides the following functionality:

- `list_display`: Specifies the fields to be displayed in the admin list view for Comment objects. In this case, it displays the task, user, and text of each comment.
- `search_fields`: Enables a search field in the admin interface to search for Comment objects by their text. """
    list_display = ('task', 'user', 'text')
    search_fields = ('text',)

# Register your models with the admin site
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
