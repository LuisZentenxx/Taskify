from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone


def home(request):
    return render(request, "home.html")


def signup(request):
    # Verifica si la solicitud es de tipo "GET"
    if request.method == "GET":
        # Si es "GET", muestra la página de registro con el formulario
        return render(request, "signup.html", {"form": UserCreationForm})

    else:
        # Verifica si las contraseñas ingresadas coinciden
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Intenta crear un nuevo usuario con los datos del formulario
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                # Guarda el usuario en la base de datos
                user.save()

                # Inicia sesión con el nuevo usuario
                login(request, user)

                # Redirige al usuario a la página "task"
                return redirect("task")

            except:
                # En caso de que haya un error al crear el usuario
                # Muestra la página de registro nuevamente con un mensaje de error
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exists"},
                )

        else:
            # Si las contraseñas ingresadas no coinciden
            # Muestra la página de registro nuevamente con un mensaje de error
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "error": "Password do not match"},
            )


def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "task.html", {'tasks': tasks})

def create_task(request):

    if request.method == 'GET':
        return render(request, "create_task.html", {
            'form' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        
        except ValueError:
            return render(request, "create_task.html", {
            'form' : TaskForm,
            'error' : 'Please provide valid date'
        })

def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task' : task, 'form' : form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task' : task, 
                                                        'form' : form,
                                                        'error' : 'Error updating task'})

def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
            })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is None:
            return render(request, "signin.html", {
                              "form": AuthenticationForm,
                              "error" : "Username or password incorrect"
                              })
        else:
            login(request, user)
            return redirect("task")
        

