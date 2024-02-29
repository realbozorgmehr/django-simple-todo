from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Todo
from .forms import TodoCreateForm, TodoUpdateForm
from django.views import View
from django.utils.text import slugify


# Create your views here.
class HomeView(View):
    def get(self, request):
        todo = Todo.objects.all()
        return render(request, 'home/home.html', context={'todos': todo})


class TodoView(View):
    def get(self, request, todo_id, todo_slug):
        todo = Todo.objects.get(id=todo_id, slug=todo_slug)
        return render(request, 'home/detail.html', context={'todo': todo})


class TodoDeleteView(View):
    def get(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        if request.user.id == todo.user.id:
            todo.delete()
            messages.success(request, 'Deleted successfully!', extra_tags='success')
            return redirect('home:home')
        else:
            messages.error(request, 'You Can\'t Delete this Todo', extra_tags='danger')
            return redirect('home:detail', todo.id, todo.slug)


class TodoCreateView(View):
    def get(self, request):
        todo = TodoCreateForm()
        return render(request, 'home/create.html', context={'form': todo})

    def post(self, request):
        todo = TodoCreateForm(request.POST)
        if todo.is_valid():
            cd = todo.cleaned_data
            Todo.objects.create(title=cd['title'], body=cd['body'], created=cd['created'])
            messages.success(request, 'todo created successfully!', 'success')
            return redirect('home:home')


class TodoUpdateView(View):
    form_class = TodoUpdateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.todo_instance = Todo.objects.get(id=kwargs['todo_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        todo = Todo.objects.get(pk=kwargs['todo_id'])
        if not request.user.id == todo.user.id:
            messages.error(request, 'You Can\'t Edit this Todo', extra_tags='danger')
            return redirect('home:detail', todo.id, todo.slug)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        todo = self.todo_instance
        form = self.form_class(instance=todo)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, todo_id):
        todo = self.todo_instance
        form = self.form_class(request.POST, instance=todo)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.slug = slugify(form.cleaned_data['title'][:30])
            new_form.save()
            messages.success(request, 'todo updated successfully', extra_tags='success')
            return redirect('home:detail', todo.id, todo.slug)
