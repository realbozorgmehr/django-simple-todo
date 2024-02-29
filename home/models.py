from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=250)
    body = models.TextField()
    slug = models.SlugField(default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('home:detail', args=(self.id, self.slug))
