from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat
from django.http import JsonResponse

@login_required
def chat_view(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chatbox.html', {'users': users, 'current_user': request.user})

@login_required
def load_chat_history(request, target_username):
    try:
        target_user = User.objects.get(username=target_username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    current_user = request.user

    # Fetch the chat history between the logged-in user and the target user
    messages = Chat.objects.filter(
        sender__in=[current_user, target_user],
        receiver__in=[current_user, target_user]
    ).order_by('timestamp')

    chat_data = []
    for msg in messages:
        chat_data.append({
            'sender': msg.sender.username,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%I:%M %p'),
        })

    return JsonResponse(chat_data, safe=False)
