from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('tasks/', TasksListViewSet.as_view()),
    path('create/', TaskCreateView.as_view({'post': 'create'})),
    path('tasks/<int:pk>', TaskUpdateView.as_view()),
    path('tasks/to-do/', TodoTasksView.as_view({'get': 'list'})),
    path('tasks/in-progress/', InProgressTasksView.as_view({'get': 'list'})),
    path('tasks/done/', DoneTasksView.as_view({'get': 'list'})),
    path('tasks/expired/', ExpiredTasksView.as_view({'get': 'list'}))
])
