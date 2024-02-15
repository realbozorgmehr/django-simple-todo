from django import forms
from .models import Todo


class TodoCreateForm(forms.Form):
    title = forms.CharField(max_length=250,
                            widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'text', 'class': 'form-control'}))
    created = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'placeholder': '2024-02-15 23:23:50.178209', 'class': 'form-control'}))


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'
