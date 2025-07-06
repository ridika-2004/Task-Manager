# Task-Manager

It's a simple system to help myself learning the overview of python django.

## Project Structure
```console
taskmanager/
├── manage.py
├── taskmanager/          # project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── tasks/                # your app
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── templates/
    │   └── tasks/
    │       ├── home.html
    │       ├── add_task.html
    │       └── update_task.html
    └── ...
```

## Start

For this you need to have `python` installed. Then run this following command in cmd
```console
pip install django
```

### Start a project & app
```console
django-admin startproject taskmanager
cd taskmanager
python manage.py startapp tasks
```

### Register app in `settings.py`
```python
INSTALLED_APPS = [
    ...,
    'tasks',
]
```

### Create the Task model
```python
# tasks/models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

### Migrate database
```console
python manage.py makemigrations
python manage.py migrate
```
### Create Views
```python
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
```
### URL Configuration
In `taskmanager/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]
```
In `tasks/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_task, name='add_task'),
    path('done/<int:task_id>/', views.mark_done, name='mark_done'),
]
```
### Templates
`home.html`
```html
<h1>Task List</h1>
<a href="{% url 'add_task' %}">Add New Task</a>
<ul>
    {% for task in tasks %}
        <li>
            {{ task.title }} - {% if task.completed %}✔{% else %}<a href="{% url 'mark_done' task.id %}">Mark Done</a>{% endif %}
        </li>
    {% endfor %}
</ul>
```
`add_task.html`
```html
<h1>Add Task</h1>
<form method="post">
    {% csrf_token %}
    <input type="text" name="title" placeholder="Task title">
    <button type="submit">Add</button>
</form>
```
## Run the Server
```console
python manage.py runserver
```
Visit `http://127.0.0.1:8000/`
