from django.shortcuts import render, get_object_or_404
# views.py
from rest_framework import generics
from django.contrib.auth.models import User  # Replace with your User model if different
from .serializers import UserSerializer

# Create your views here.
def chatbox(request):
    # # chat_user = get_object_or_404(User, username=username)
    # messages = ChatMessage.objects.filter(room_name=request.user.username + chat_user.username) | \
    #            ChatMessage.objects.filter(room_name=chat_user.username + request.user.username)
    # messages = messages.order_by('timestamp')
    
    return render(request, 'chatbox.html')




class UserListView(generics.ListAPIView):
    queryset = User.objects.all()  # Modify if you want to filter users
    serializer_class = UserSerializer
