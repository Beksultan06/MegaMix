from django.db import models

# Create your models here.

class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    has_started = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username or self.first_name or self.user_id}"