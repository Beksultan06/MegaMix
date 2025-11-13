import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.crypto import get_random_string

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import Chat

        self.chat_id = self.scope['url_route']['kwargs'].get('chat_id')
        if not self.chat_id:
            self.chat_id = get_random_string(10)
            await self.send(json.dumps({"chat_id": self.chat_id}))

        self.room_group_name = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        from .models import Chat, Message

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON"}))
            return

        text = data.get("text")
        sender = data.get("sender")
        if not text or not sender:
            await self.send(json.dumps({"error": "Missing 'text' or 'sender'"}))
            return

        # Асинхронно создаём или получаем чат
        chat = await self.get_or_create_chat(self.chat_id)

        # Асинхронно создаём сообщение
        await self.create_message(chat, sender, text)

        # Отправляем сообщение всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "text": text,
                "sender": sender,
            }
        )

    async def chat_message(self, event):
        # Отправляем сообщение клиенту
        await self.send(text_data=json.dumps({
            "text": event["text"],
            "sender": event["sender"],
        }))

    # -------------------------
    # Методы для работы с ORM
    # -------------------------

    @database_sync_to_async
    def get_or_create_chat(self, chat_id):
        from .models import Chat
        chat, _ = Chat.objects.get_or_create(user_uid=chat_id)
        return chat

    @database_sync_to_async
    def create_message(self, chat, sender, text):
        from .models import Message
        return Message.objects.create(chat=chat, sender=sender, text=text)
