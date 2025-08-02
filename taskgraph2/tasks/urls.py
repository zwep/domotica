from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_graph, name='task_graph'),
    path('task/<int:task_id>/action/', views.task_action, name='task_action'),
]
