from django.urls import path

from api.views import *

urlpatterns = [
    path('task-list/', taskList, name='read'),
    path('task-create/', taskCreate, name='create'),
    path('task/<str:pk>/', taskItem, name='item'),
]


