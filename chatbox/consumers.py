from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Chat
from encryption.encrypt_test import encrypt_message, decrypt_message
import pytz  # For timezone handling
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):

    """
    The `ChatConsumer` class is an asynchronous WebSocket consumer that handles real-time chat functionality in a Django Channels-based application.

    The class provides the following functionality:

    - `connect`: Joins the user to a chat room group based on the room name and the user's username.
    - `disconnect`: Leaves the user from the chat room group when the WebSocket connection is closed.
    - `receive`: Handles incoming messages from the WebSocket, encrypts the message, saves it to the database, and sends the message to the chat 
    room group.
    - `chat_message`: Handles incoming messages from the chat room group, decrypts the message, converts the timestamp to the Indian timezone 
    (Asia/Kolkata), and sends the message to the WebSocket.

    The class uses the `encrypt_message` and `decrypt_message` functions from the `encryption.encrypt_test` module to encrypt and decrypt the
    chat messages, respectively. It also uses the `sync_to_async` function from `asgiref.sync` to interact with the Django ORM in an asynchronous
    context.
    """

    async def connect(self):
        self.room_name = '-'.join(sorted([self.scope['user'].username, self.scope['url_route']['kwargs']['room_name']]))
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_username = data['receiver']

        receiver = await sync_to_async(User.objects.get)(username=receiver_username)

        # Encrypt the message
        encrypted_message = encrypt_message(message)

        # Save the message to the database
        chat_message = await sync_to_async(Chat.objects.create)(
            sender=self.scope['user'], receiver=receiver, message=encrypted_message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat_message.message,  # This is encrypted
                'sender': chat_message.sender.username,
                'timestamp': chat_message.timestamp  # Keep as UTC
            }
        )

    async def chat_message(self, event):
        encrypted_message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Decrypt the message before sending it to WebSocket
        decrypted_message = decrypt_message(encrypted_message)

        # Convert the timestamp to Indian timezone (Asia/Kolkata)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        formatted_timestamp = timestamp.astimezone(indian_timezone).strftime('%I:%M %p')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': decrypted_message,
            'sender': sender,
            'timestamp': formatted_timestamp  # Convert to IST for display
        }))
