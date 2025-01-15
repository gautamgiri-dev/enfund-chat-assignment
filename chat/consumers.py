import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    online_users = set()

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['user'].username
        self.online_users.add(self.room_name)
        self.user_status_group_name = 'user_status'

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            self.user_status_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'online_users',
            'users': list(self.online_users)
        }))

        # # Notify group that a user has connected
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'user_connected',
        #         'username': self.scope["user"].username
        #     }
        # )

        # Broadcast to all users that this user is online
        await self.channel_layer.group_send(
            self.user_status_group_name,
            {
                'type': 'user_status',
                'username': self.scope["user"].username,
                'status': 'online'
            }
        )

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.user_status_group_name,
            self.channel_name
        )

        # Notify group that a user has disconnected
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'user_disconnected',
        #         'username': self.scope["user"].username
        #     }
        # )

        # Broadcast to all users that this user is offline
        await self.channel_layer.group_send(
            self.user_status_group_name,
            {
                'type': 'user_status',
                'username': self.scope["user"].username,
                'status': 'offline'
            }
        )

        self.online_users.remove(self.room_name)

    async def receive(self, text_data):
        event = json.loads(text_data)

        if event.get('type') == 'send_message':
            message = event['message']
            receiver_username = event['to']

            # Save the message to the database
            sender = self.scope['user']
            receiver = await database_sync_to_async(User.objects.get)(username=receiver_username)
            await database_sync_to_async(Message.objects.create)(sender=sender, receiver=receiver, message=message)

            await self.channel_layer.group_send(
                receiver_username,
                {
                    'type': 'chat_message',
                    'message': message,
                    'from': sender.username
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_connected(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_disconnected(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_status(self, event):
        await self.send(text_data=json.dumps(event))