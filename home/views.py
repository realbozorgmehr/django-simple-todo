from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Todo
from .forms import TodoCreateForm, TodoUpdateForm
from django.views import View


# Create your views here.
class HomeView(View):
    def get(self, request):
        todo = Todo.objects.all()
        return render(request, 'home.html', context={'todos': todo})


class TodoView(View):
    def get(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        return render(request, 'detail.html', context={'todo': todo})


class TodoDeleteView(View):
    def get(self, request, todo_id):
        Todo.objects.get(id=todo_id).delete()
        messages.success(request, 'todo deleted successfully!', 'success')
        return redirect('home:home')


class TodoCreateView(View):
    def post(self, request):
        todo = TodoCreateForm(request.POST)
        if todo.is_valid():
            cd = todo.cleaned_data
            Todo.objects.create(title=cd['title'], body=cd['body'], created=cd['created'])
            messages.success(request, 'todo created successfully!', 'success')
            return redirect('home:home')

    def get(self, request):
        todo = TodoCreateForm()
        return render(request, 'create.html', context={'form': todo})


def update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if request.method == 'POST':
        form = TodoUpdateForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'todo updated successfully!', 'success')
            return redirect('home:detail', todo_id)
    else:
        form = TodoUpdateForm(instance=todo)
    return render(request, 'update.html', context={'form': form})
