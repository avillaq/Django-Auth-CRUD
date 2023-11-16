from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):

    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        # Si es get muestrame el formulario
        return render(request, 'signup.html', {
            "form" : UserCreationForm
        })
    
    # Si es post, crea el usuario
    if request.POST['password1'] == request.POST['password2']:
        try:
            # Crear el usuario
            user = User.objects.create_user(
                request.POST['username'], 
                password=request.POST['password1']
            )
            # Guardar el usuario
            user.save()
            # Loguear al usuario y mantenerlo logueado (sesion)
            login(request, user)
            return redirect('tasks')
        
        except Exception as e:
            return render(request, 'signup.html', {
                "form" : UserCreationForm,
                "error" : "Username already exists"
            })
    
    return render(request, 'signup.html', {
                "form" : UserCreationForm,
                "error" : "Passwords do not match"
            })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        "tasks" : tasks
    })
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'tasks.html', {
        "tasks" : tasks
    })

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html',{
            "form" : TaskForm
        })
    try:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('tasks')
    
    except Exception as e:
        return render(request, 'create_task.html',{
            "form" : TaskForm,
            "error" : "Bad data passed in. Try again."
        })
        
@login_required
def task_detail(request,id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=id, user = request.user)
        form = TaskForm(instance=task)

        return render(request, 'task_detail.html', {
            "task" : task,
            "form": form
        })
    try:
        task = get_object_or_404(Task, pk=id, user = request.user)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks')
    
    except Exception as e:
        return render(request, 'task_detail.html', {
            "task" : task,
            "form": form,
            "error" : "Error updating task. Try again."
        })

@login_required
def task_complete(request,id):
    task = get_object_or_404(Task, pk=id, user = request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_delete(request,id):
    task = get_object_or_404(Task, pk=id, user = request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html',{
            "form" : AuthenticationForm
        })
    
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    
    if user is None:
        return render(request, 'signin.html',{
                "form" : AuthenticationForm,
                "error" : "Username or password did not match"
            })

    login(request, user)
    return redirect('tasks')
