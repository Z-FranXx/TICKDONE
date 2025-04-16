"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.session_begin, name="login"),
    path('logout/',views.close_session, name="logout"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/completed', views.tasks_completed, name="tasks_completed"),
    path('tasks/create/', views.create_task, name="create_tasks"),
    path('tasks/<int:task_id>/', views.task_info, name='task_info'),
    path('tasks/<int:task_id>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    
]
