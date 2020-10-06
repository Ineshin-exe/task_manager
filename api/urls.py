from django.urls import path

from api.views import *

urlpatterns = [
    path('task-list/', task_list, name='read'),
    path('task-create/', task_create, name='create'),
    path('task/<str:pk>/', task_item, name='item'),
    path('task/<str:pk>/changelog/', task_changelog, name='changelog'),
]


