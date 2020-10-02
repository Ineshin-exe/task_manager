import json

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, unique=True)
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
        return str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        changes = {
            "title": self.title,
            "description": self.description,
            "deadline": str(self.deadline),
            "status": self.status
        }

        ChangeLogTask.objects.create(task=Task.objects.get(id=self.id),
                                     data=changes)


class ChangeLogTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, unique=True)
    changeTime = models.DateTimeField(null=True, auto_now_add=True)
    data = models.JSONField(null=True)

    def __str__(self):
        return '{}[{}] at {}'.format(self.task.title, self.task.id, self.changeTime.strftime('%Y-%m-%d %H:%M:%S'))