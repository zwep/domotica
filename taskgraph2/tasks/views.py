from django.shortcuts import render, get_object_or_404, redirect
from .models import Task

def task_graph(request):
    tasks = Task.objects.prefetch_related('depends_on').all()
    return render(request, 'task_graph.html', {'tasks': tasks})

def task_action(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    print(f"Task clicked: {task.name}")
    return redirect('task_graph')
