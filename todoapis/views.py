import logging
import traceback
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework import status
from .serializers import TaskSerializer
from .models import Task

logger = logging.getLogger('api_logs')


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task-list/',
        'Detail View' : '/task-detail/<str:pk>/',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete/<str:pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskList(request):
    try:
        user = request.user
        cached_data = cache.get_or_set(user.id, Task.objects.filter(created_by=user))
        tasks = cached_data
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data)
    except Exception as e:
        logger.error("taskList: {}".format(traceback.format_exc()))
        return Response({
            "error": list(e.args)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskDetail(request, pk):
    try:
        cached_data = cache.get_or_set(pk, Task.objects.get(id=pk))
        tasks = cached_data
        print(tasks.__dict__)
        if tasks.created_by_id == request.user.id:
            serializer = TaskSerializer(tasks, many = False)
            return Response(serializer.data)
        return Response({"error": "Unauthorised"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        logger.error("taskDetail: {}".format(traceback.format_exc()))
        return Response({
            "error": list(e.args)
        }, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def taskUpdate(request, pk):
    try:
        task = Task.objects.get(id = pk)
        if task.created_by == request.user:
            serializer = TaskSerializer(instance=task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.set(pk, task)
            return Response(serializer.data)
        return Response({"error": "Unauthorised"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        logger.error("taskUpdate: {}".format(traceback.format_exc()))
        return Response({
            "error": list(e.args)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def taskCreate(request):
    try:
        if request.data.get('created_by') == request.user.id:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                task = serializer.save()
                all_tasks = Task.objects.filter(created_by=request.user)
                cache.set(request.user.id, all_tasks)
                cache.set(task.id, task)
            return Response(serializer.data)

        return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("taskCreate: {}".format(traceback.format_exc()))
        return Response({
            "error": list(e.args)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def taskDelete(request, pk):
    try:
        task = Task.objects.get(id = pk)
        if task.created_by == request.user:
            cache.delete(task.id)
            task.delete()
            all_tasks = Task.objects.filter(created_by=request.user)
            cache.set(request.user.id, all_tasks)
            return Response("Taks deleted successfully.")
        return Response({"error": "Unauthorised"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        logger.error("taskDelete: {}".format(traceback.format_exc()))
        return Response({
            "error": list(e.args)
        }, status=status.HTTP_400_BAD_REQUEST)