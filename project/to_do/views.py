from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend

from .service import TaskFilter
from .models import Tasks
from .serializer import (
    TaskSerializer,
    TaskCreateOrSerializer
)

from datetime import date


# class TasksListView(APIView):
#
#
#     def get(self, request):
#         model = Tasks.objects.all()
#         serializer = TaskSerializer(model, many=True)
#         return Response(serializer.data)


class TasksListViewSet(generics.ListAPIView):
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task = Tasks.objects.all()
        return task


# class TaskCreateView(APIView):
#
#     def post(self, request):
#         serializer = TaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=201)
#         else:
#             return Response(status=401)

class TaskCreateView(viewsets.ModelViewSet):
    serializer_class = TaskCreateOrSerializer


class TaskUpdateView(APIView):

    def get(self, request, pk):
        if Tasks.objects.get(pk=pk):
            model = Tasks.objects.get(pk=pk)
            serializer = TaskCreateOrSerializer(model)
            return Response(serializer.data)
        else:
            return Response(status=404)

    def put(self, request, pk):
        if Tasks.objects.get(pk=pk):
            model = Tasks.objects.get(pk=pk)
            serializer = TaskCreateOrSerializer(model, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response(status=401)
        else:
            return Response(status=404)

    def patch(self, request, pk):
        if Tasks.objects.get(pk=pk):
            model = Tasks.objects.get(pk=pk)
            serializer = TaskCreateOrSerializer(model, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response(status=401)
        else:
            return Response(status=404)

    def delete(self, request, pk):
        if Tasks.objects.get(pk=pk):
            model = Tasks.objects.get(pk=pk)
            model.delete()
            return Response(status=404)
        else:
            return Response(status=404)


# class TaskUpdateView(generics.UpdateAPIView):
#     queryset = Tasks.objects.all()
#     serializer_class = TaskUpdateSerializer
#     lookup_field = 'pk'

# class TaskUpdateView(viewsets.ModelViewSet):
#     queryset = Tasks.objects.all()
#     serializer_class = TaskUpdateSerializer
#     lookup_field = 'pk'
#     queryset.destroy()
#
#     def destroy(self, request, *args, **kwargs):
#         model_object = self.get_object()
#         self.perform_destroy(model_object)
#         return Response(status=204)

class TodoTasksView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    queryset = Tasks.objects.filter(status=Tasks.todo)


class InProgressTasksView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    queryset = Tasks.objects.filter(status='in progress')


class DoneTasksView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    queryset = Tasks.objects.filter(status='done')


class ExpiredTasksView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    queryset = Tasks.objects.filter(end_time__lt=str(date.today()))
