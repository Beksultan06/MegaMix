from django.db import models
from django.conf import settings

class Chat(models.Model):
    user_uid = models.CharField(max_length=100, unique=True, verbose_name="ID пользователя")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат {self.user_uid}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=50, choices=(("user", "Пользователь"), ("manager", "Менеджер")))
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_manager": True},
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}"
