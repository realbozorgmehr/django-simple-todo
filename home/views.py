from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Todo
from .forms import TodoCreateForm, TodoUpdateForm


# Create your views here.
def home(request):
    todo = Todo.objects.all()
    return render(request, 'home.html', context={'todos': todo})


def detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    return render(request, 'detail.html', context={'todo': todo})


# managing todos
def delete(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    messages.success(request, 'todo deleted successfully!', 'success')
    return redirect('home')


def create(request):
    if request.method == 'POST':
        todo = TodoCreateForm(request.POST)
        if todo.is_valid():
            todo.save()
            messages.success(request, 'todo created successfully!', 'success')
            return redirect('home')
    else:
        todo = TodoCreateForm()
    return render(request, 'create.html', context={'form': todo})


def update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if request.method == 'POST':
        form = TodoUpdateForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'todo updated successfully!', 'success')
            return redirect('detail', todo_id)
    else:
        form = TodoUpdateForm(instance=todo)
    return render(request, 'update.html', context={'form': form})

