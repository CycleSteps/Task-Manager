from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Chat
from encryption.encrypt_test import encrypt_message,decrypt_message




class ChatConsumer(AsyncWebsocketConsumer):

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
        sender = data['sender']
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
                'timestamp': chat_message.timestamp.strftime('%I:%M %p')
            }
        )

    async def chat_message(self, event):
        encrypted_message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Decrypt the message before sending it to WebSocket
        decrypted_message = decrypt_message(encrypted_message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': decrypted_message,
            'sender': sender,
            'timestamp': timestamp
        }))
