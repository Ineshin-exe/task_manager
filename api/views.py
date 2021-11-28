from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import TaskSerializer, ChangeLogTaskSerializer
from .models import Task, ChangeLogTask


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    list = Task.objects.filter(owner=request.user)
    params = request.query_params

    for filter in params.dict():
        if filter == 'status':
            list = list.filter(status=params[filter])
        elif filter == 'deadline':
            list = list.filter(deadline=params[filter])
        else:
            return Response({'message': 'filter \'{}\' is not supported'.format(filter)},
                            status=status.HTTP_400_BAD_REQUEST)

    serializer = TaskSerializer(list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):

    serializer = TaskSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save(owner=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_item(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if not task.owner == request.user:
        return Response({'message': 'You are not a owner of this task.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = TaskSerializer(instance=task, data=request.data)

        if not request.data:
            return Response({'message': 'No data to update'}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task was deleted successfully!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_changelog(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    log = ChangeLogTask.objects.filter(task=task)
    serializer = ChangeLogTaskSerializer(log, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)