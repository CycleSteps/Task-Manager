from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat
from django.http import JsonResponse
from encryption.encrypt_test import encrypt_message,decrypt_message
import pytz  # For timezone handling



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
        decrypted_message = decrypt_message(msg.message)  # Decrypt the message
        
        # Convert timestamp to IST for display
        indian_timezone = pytz.timezone('Asia/Kolkata')
        formatted_timestamp = msg.timestamp.astimezone(indian_timezone).strftime('%I:%M %p')

        chat_data.append({
            'sender': msg.sender.username,
            'message': decrypted_message,
            'timestamp': formatted_timestamp,  # Display in IST
        })

    return JsonResponse(chat_data, safe=False)

