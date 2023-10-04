from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login

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
                user = User.objects.create(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                # Guarda el usuario en la base de datos
                user.save()
                
                # Inicia sesión con el nuevo usuario
                login(request, user)
                
                # Redirige al usuario a la página "task"
                return redirect('task')
            
            except:
                # En caso de que haya un error al crear el usuario
                # Muestra la página de registro nuevamente con un mensaje de error
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm,
                     "error": "Username already exists"},
                )

        else:
            # Si las contraseñas ingresadas no coinciden
            # Muestra la página de registro nuevamente con un mensaje de error
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm,
                 "error": "Password do not match"},
            )

def task(request):
    return render(request, "task.html")