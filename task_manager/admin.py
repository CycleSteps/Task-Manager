from django.contrib import admin
from task_manager.models import Project, Task,Subtask, Comment



class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1  # Number of empty forms to display

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty forms to display




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
    list_display = ('task', 'description', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('description',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'text')
    search_fields = ('text',)

# Register your models with the admin site
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
