from datetime import date

from rest_framework import serializers

from .models import Task, ChangeLogTask


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    deadline = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = Task
        fields = (
            'owner', 'id', 'title', 'description', 'createdAt',
            'deadline', 'status'
        )


class ChangeLogTaskSerializer(serializers.ModelSerializer):
    changeTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = ChangeLogTask
        fields = (
            '__all__'
        )