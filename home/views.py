from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Todo
from .forms import TodoCreateUpdateForm
from django.views import View
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class HomeView(View):
    def get(self, request):
        todo = Todo.objects.all()
        return render(request, 'home/home.html', context={'todos': todo})


class TodoView(View):
    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs['todo_id'], slug=kwargs['todo_slug'])
        return render(request, 'home/detail.html', context={'todo': todo})


class TodoDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs['todo_id'])
        if request.user.id == todo.user.id:
            todo.delete()
            messages.success(request, 'Deleted successfully!', extra_tags='success')
            return redirect('home:home')
        else:
            messages.error(request, 'You Can\'t Delete this Todo', extra_tags='danger')
            return redirect('home:detail', todo.id, todo.slug)


class TodoCreateView(LoginRequiredMixin, View):
    form_class = TodoCreateUpdateForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.slug = slugify(form.cleaned_data['title'][:30])
            new_todo.save()
            messages.success(request, 'Todo created successfuly', extra_tags='success')
            return redirect('home:detail', new_todo.id, new_todo.slug)


class TodoUpdateView(LoginRequiredMixin, View):
    form_class = TodoCreateUpdateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.todo_instance = get_object_or_404(Todo, pk=kwargs['todo_id'])
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

    def post(self, request, *args, **kwargs):
        todo = self.todo_instance
        form = self.form_class(request.POST, instance=todo)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.slug = slugify(form.cleaned_data['title'][:30])
            new_form.save()
            messages.success(request, 'todo updated successfully', extra_tags='success')
            return redirect('home:detail', todo.id, todo.slug)
