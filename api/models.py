from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(default='Undefined', max_length=64)
    description = models.TextField(default='No description.')
    createdAt = models.DateTimeField(null=True, auto_now_add=True)
    deadline = models.DateField(null=True)

    class Status(models.TextChoices):
        NEW = 'New'
        PLANNED = 'Planned'
        IN_PROGRESS = 'In progress'
        COMPLETED = 'Completed'

    status = models.TextField(choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return self.title