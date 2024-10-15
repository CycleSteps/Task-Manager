from django.urls import path
from .views import Projects, Tasks, ManegeTasks, MangeProject,UpdateSubtaskStatusView, AddCommentView,AddSubtaskView,TaskFiles,DownloadFileView
from . import views

urlpatterns = [
    path('', Projects.as_view(), name='boards'),
    path('<id>', Tasks.as_view(), name='tasks'),
    path('<id>/delete', MangeProject.as_view()),
    path('<id>/task', ManegeTasks.as_view()),
    path('update-subtask-status/', UpdateSubtaskStatusView.as_view(), name='update_subtask_status'),
    path('add-comment/', AddCommentView.as_view(), name='add_comment'),
    path('add-subtask/', AddSubtaskView.as_view(), name='add_subtask'),
    path('update-subtask-status/', UpdateSubtaskStatusView.as_view(), name='update_subtask_status'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('document/<int:task_id>/', TaskFiles.as_view(), name='upload_document'),
    path('document/<int:task_id>/<int:file_id>/download/', views.DownloadFileView, name='download_document'),
    path('delete-document/<int:document_id>/', views.delete_document, name='delete_document'),
    path('delete_all_documents/<int:task_id>/', views.delete_all_documents, name='delete_all_documents'),
    path('<int:id>/update-title/', views.update_task_title, name='update_task_title'),
    path('<int:id>/update-description/', views.update_task_description, name='update_task_description'),
    path('reassign_task/<int:task_id>/', views.reassign_task, name='reassign_task'),
    path('get_assigned_users/<int:task_id>/', views.get_assigned_users, name='get_assigned_users'),
]

