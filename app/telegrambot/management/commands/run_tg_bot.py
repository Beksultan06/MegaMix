from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from django.conf import settings
from app.telegrambot.models import TelegramUser
from asgiref.sync import sync_to_async
import asyncio

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        user_id=message.from_user.id
    )

    user.username = message.from_user.username
    user.first_name = message.from_user.first_name
    user.has_started = True
    await sync_to_async(user.save)()

    await message.answer("👋 Привет! Теперь вы будете получать уведомления о заказах!")

class Command(BaseCommand):
    help = "Запуск Telegram-бота"

    def handle(self, *args, **options):
        asyncio.run(dp.start_polling(bot))
