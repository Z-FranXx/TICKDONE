from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages
from django.forms import ModelForm
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

# Solicitud pantalla de inicio
def home(request):
    return render(request, 'page/home.html')

# Solicitud para registrarse
def signup(request):

    if request.method == "GET":
        return render(request, 'auth/signup.html', {
        'form': UserCreationForm
    })
    else:
        # La contraseña tiene que ser igual a la confirmacion
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crear el usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                # Redireccionar a la pagina de tareas
                return redirect('tasks')
            # Si el usuario ya existe, mostrar error
            except IntegrityError:
                return render(request, 'auth/signup.html', {
                'form': UserCreationForm,
                'error': "El usuario ya existe."
            })
        # Si la contraseña no coincide, mostrar error
        else:
            # Si la contraseña no coincide, mostrar error
            messages.error(request, "Las contraseñas no coinciden.")
            # Volver a renderizar el formulario de registro 
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': "Contraseña no coincide."
            })

# Función para iniciar sesion (login) de un usuario
def session_begin(request):
    # Si la solicitud es de tipo GET, se muestra el formulario de login vacio
    if request.method == "GET":
        return render(request, 'auth/login.html', {
            'form': AuthenticationForm  # Se pasa el formulario de autenticacion al template
        })
    else:
        # Si la solicitud es de tipo POST, se intenta autenticar al usuario con las credenciales enviadas
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        
        # Si la autenticacion falla (usuario no valido)
        if user is None:
            # Se muestra un mensaje de error
            messages.error(request, "Usuario o contraseña incorrectos.")
            # Se vuelve a renderizar el formulario con el error
            return render(request, 'auth/login.html', {
                'form': AuthenticationForm,
                'error': "Usuario o contraseña incorrectos."
            })
        else:
            # Si el usuario es valido, se inicia la sesion
            login(request, user)
            # Y se redirige a la vista 'tasks' 
            return redirect('tasks')

# Solicitud para cerrar sesión
@login_required  # Requiere que el usuario este autenticado para acceder a esta vista
def close_session(request):
    logout(request)
    return redirect('home')

# Direccionar a la pagina de tareas pendientes
@login_required  # Requiere que el usuario este autenticado para acceder a esta vista
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)  # Filtra las tareas del usuario autenticado
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks  # Pasa las tareas al frontend (template)
    })

# Direccionar a la pagina de tareas completadas
@login_required  # Requiere que el usuario este autenticado para acceder a esta vista
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by # Filtra las tareas del usuario autenticado
    ('-datecompleted')  
    return render(request, 'tasks/tasks_completed.html', {
        'tasks': tasks  # Pasa las tareas al frontend (template)
    })

# Rederizar la pagina de tareas
@login_required  # Requiere que el usuario este autenticado para acceder a esta vista
def create_task(request):
    if request.method == "GET":
        # Si la solicitud es GET, renderiza el formulario vacio para que el usuario lo complete
        return render(request, 'tasks/create_tasks.html', {
            'form': TaskForm()  # Se pasa el formulario vacio al frontend (template))
        })

    else:
        try:
            # Si la solicitud es POST, se procesa el formulario con los datos enviados
            form = TaskForm(request.POST)

            # Verifica si el formulario es valido antes de guardar la tarea
            if form.is_valid():
                # Se guarda la tarea sin confirmarla aun, para poder agregar informacion adicional
                new_task = form.save(commit=False)
                new_task.user = request.user  # Se asigna el usuario autenticado como creador de la tarea
                new_task.save()  # Guarda la tarea en la base de datos

                # Redirige a la vista de lista de tareas
                return redirect('tasks')

            else:
                # Si el formulario no es valido, muestra el formulario con los errores
                return render(request, 'create_tasks.html', {
                    'form': form,
                    'error': "Por favor, revisa los errores en el formulario."
                })

        except ValueError:
            # Si ocurre un error al guardar (por ejemplo, un error de validacion), muestra un mensaje de error
            return render(request, 'create_tasks.html', {
                'form': TaskForm(),  # Se pasa el formulario vacio al frontend (template))
                'error': "Error al crear la tarea. Por favor, verifica los datos ingresados."
            })

# Rederizar la pagina de actualizar tarea
@login_required  # Requiere que el usuario este autenticado para acceder a esta vista
def task_info(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)  # Obtiene la tarea por su ID y el usuario autenticado
        form = TaskForm(instance=task)  # Crea un formulario con los datos de la tarea
        return render(request, 'tasks/task_info.html', {
            'task': task,  # Pasa la tarea al template
            'form': form  # Pasa el formulario al template
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)  # Obtiene la tarea por su ID y el usuario autenticado
            form = TaskForm(request.POST, instance=task)  # Crea un formulario con los datos de la tarea
            form.save()  # Guarda los cambios en la tarea
            return redirect('tasks')  # Redirige a la vista de tareas  
        except ValueError:
            return render(request, 'task_info.html', {
            'task': task,  # Pasa la tarea al template
            'form': form,  # Pasa el formulario al template
            'error': "Error al actualizar la tarea. Por favor, verifica los datos ingresados."
        })

# Marcar tarea como completada
@login_required  # Requiere que el usuario este autenticado para acceder a esta vista
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Obtiene la tarea por su ID y el usuario autenticado
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()  # Guarda la tarea con la fecha de completado
        return redirect('tasks')

# Eliminar tarea
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Obtiene la tarea por su ID y el usuario autenticado
    if request.method == 'POST':
        task.delete()  # Elimina la tarea de la base de datos
        return redirect('tasks')

    
