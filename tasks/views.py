# tasks/views.py
from django.shortcuts import render, redirect
from .models import Task

def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks': tasks})

def add_task(request):
    if request.method == "POST":
        title = request.POST['title']
        Task.objects.create(title=title)
        return redirect('home')
    return render(request, 'tasks/add_task.html')

def mark_done(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('home')
