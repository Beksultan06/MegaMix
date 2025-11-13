from aiogram import Bot
from django.conf import settings
from app.telegrambot.models import TelegramUser

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

async def send_message_to_all(text: str):
    users = TelegramUser.objects.filter(has_started=True)
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id, text=text)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user.user_id}: {e}")
