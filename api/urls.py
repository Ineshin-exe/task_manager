from django.urls import path

from api.views import *

urlpatterns = [
    path('tasks/', task_list, name='read'),
    path('tasks/', task_create, name='create'),
    path('tasks/<str:pk>/', task_item, name='item'),
    path('tasks/<str:pk>/changelog/', task_changelog, name='changelog'),
]


