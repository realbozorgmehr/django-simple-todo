from django import forms
from .models import Todo


class TodoCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'body')
