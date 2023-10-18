from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/create/', views.create_task, name='create_task'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
]
