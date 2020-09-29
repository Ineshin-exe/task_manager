from django.urls import path

from api.views import *

urlpatterns = [
    path('task-list/', taskList),
    path('task-create/', taskCreate),
    path('task-update/<str:pk>/', taskUpdate),
]


