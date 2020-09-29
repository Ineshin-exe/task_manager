from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    class Status(models.TextChoices):
        NEW = 'Новая'
        PLANNED = 'Запланированная'
        IN_PROGRESS = 'В работе'
        COMPLETED = 'Завершённая'

    status = models.TextField(choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return self.title