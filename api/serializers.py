from datetime import date

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task, ChangeLogTask


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    deadline = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = Task
        fields = (
            'owner', 'id', 'title', 'description', 'created_at',
            'deadline', 'status'
        )


class ChangeLogTaskSerializer(serializers.ModelSerializer):
    change_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = ChangeLogTask
        fields = (
            'task', 'change_time', 'data'
        )