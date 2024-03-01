from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from home.models import Todo
from django.urls import reverse_lazy
from django.contrib.auth import views as authviews


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
            messages.success(request, 'Account created successfully!', extra_tags='success')
            return redirect('home:home')
        return render(request, self.template_name, context={'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully!', extra_tags='success')
                return redirect('home:home')
            else:
                messages.error(request, "username or password is wrong", extra_tags='danger')
        return render(request, self.template_name, context={"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logged out successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        todos = Todo.objects.filter(user=user)
        return render(request, 'accounts/profile.html', context={'user': user, 'todos': todos})


class UserPasswordResetView(authviews.PasswordResetView):
    template_name = 'accounts/reset-password/password_reset.html'
    success_url = reverse_lazy('accounts:user_password_reset_done')
    email_template_name = 'accounts/reset-password/password_reset_email.html'


class UserPasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = 'accounts/reset-password/password_reset_done.html'


class UserPasswordResetConfirmView(authviews.PasswordResetConfirmView):
    template_name = 'accounts/reset-password/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:user_password_reset_complete')


class UserPasswordResetCompleteView(authviews.PasswordResetCompleteView):
    template_name = 'accounts/reset-password/password_reset_complete.html'
