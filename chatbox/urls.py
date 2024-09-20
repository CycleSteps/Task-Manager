from django.urls import path
from . import views
from .views import UserListView


urlpatterns = [
    path('chat/',views.chatbox,name="chat" ),
    path('api/users/', UserListView.as_view(), name='user-list'),
]