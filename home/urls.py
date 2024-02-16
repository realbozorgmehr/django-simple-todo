from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # managing todos
    path('<int:todo_id>/', views.TodoView.as_view(), name='detail'),
    path('create/', views.TodoCreateView.as_view(), name='create'),
    path('update/<int:todo_id>/', views.TodoUpdateView.as_view(), name='update'),
    path('delte/<int:todo_id>/', views.TodoDeleteView.as_view(), name='delete'),
]
