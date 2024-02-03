from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # managing todos
    path('<int:todo_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('update/<int:todo_id>/', views.update, name='update'),
    path('delte/<int:todo_id>/', views.delete, name='delete'),
]
