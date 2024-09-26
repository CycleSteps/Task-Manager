from django.urls import path
from .views import Projects, Tasks, ManegeTasks, MangeProject,UpdateSubtaskStatusView, AddCommentView,AddSubtaskView,TaskFiles,DownloadFileView
from . import views

urlpatterns = [
    path('', Projects.as_view(), name='boards'),
    path('<id>', Tasks.as_view(), name='tasks'),
    path('<id>/delete', MangeProject.as_view()),
    # path('<id>', Tasks.as_view(), name='tasks'),
    path('update-subtask-status/', UpdateSubtaskStatusView.as_view(), name='update_subtask_status'),
    path('add-comment/', AddCommentView.as_view(), name='add_comment'),
    path('add-subtask/', AddSubtaskView.as_view(), name='add_subtask'),
    path('update-subtask-status/', UpdateSubtaskStatusView.as_view(), name='update_subtask_status'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('document/<int:task_id>/', TaskFiles.as_view(), name='upload_document'),
    path('document/<int:task_id>/<int:file_id>/download/', views.DownloadFileView, name='download_document'),
]
