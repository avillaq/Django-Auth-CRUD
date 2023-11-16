from django.urls import  path
from .  import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:id>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:id>/delete/', views.task_delete, name='task_delete'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),



]