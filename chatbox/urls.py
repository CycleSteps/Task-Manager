from django.urls import path
from . import views
from . import consumers


# urls.py
urlpatterns = [
    path('chat/', views.chat_view, name="chat"),
    path('load-chat-history/<str:target_username>/', views.load_chat_history, name='load_chat_history'),  # Ensure this matches in your fetch
    path('', include('smartshare.urls')),
]

