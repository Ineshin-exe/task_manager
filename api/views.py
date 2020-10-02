from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import TaskSerializer, ChangeLogTaskSerializer
from .models import Task, ChangeLogTask


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskList(request):
    list = Task.objects.filter(owner=request.user)
    params = request.query_params

    for filter in params.dict():
        if filter == 'status':
            list = list.filter(status=params[filter])
        elif filter == 'deadline':
            list = list.filter(deadline=params[filter])
        else:
            return Response({'message': 'filter \'{}\' is not supported'.format(filter)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = TaskSerializer(list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def taskCreate(request):

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def taskItem(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        serializer = TaskSerializer(instance=task, data=request.data)
        if request.data:
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No data to update'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task was deleted successfully!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskChangelog(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except:
        return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    log = ChangeLogTask.objects.filter(task=task)
    serializer = ChangeLogTaskSerializer(log, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)