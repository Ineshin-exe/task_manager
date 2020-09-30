from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task


@api_view(['GET'])
def taskList(request):
    list = Task.objects.filter(owner=request.user)

    status = request.query_params.get('status', None)
    deadline = request.query_params.get('deadline', None)
    if status is not None:
        list = list.filter(status=status)
    if deadline is not None:
        list = list.filter(deadline=deadline)

    serializer = TaskSerializer(list, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'POST', 'DELETE'])
def taskItem(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task was deleted successfully!'})