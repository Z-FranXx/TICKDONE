# TickDone ✅

**TickDone** es una aplicación web para gestionar tus tareas diarias (to-do list) desarrollada con **Python** y el framework **Django**. 
Esta aplicación permite a los usuarios agregar, editar, marcar como completadas y eliminar tareas. Además, cada usuario puede gestionar su propia lista de tareas a través de un sistema de autenticación.

## Características
- **Registro e inicio de sesión** de usuarios, con autenticación.
- **CRUD de tareas**: crear, leer, actualizar y eliminar tareas.
- **Visualización personalizada**: cada usuario puede ver y gestionar sus propias tareas.
- **Panel de administración de Django** para gestionar tareas y usuarios desde el backend.
- **Diseño moderno** usando **Bootstrap**.

![Pantalla principal de tareas]

## Tecnologías utilizadas
- **Python**  
- **Django**  
- **Bootstrap**  
- **PostgreSQL** (usado en Render para la base de datos)  
- **Virtualenv** para el entorno virtual

## Despliegue en Render
La aplicación está desplegada en **Render**, una plataforma para hosting de aplicaciones web. Puedes acceder a la app directamente desde [aquí](https://tickdone.onrender.com).

## Instalación y ejecución local

1. Clona el repositorio:
    ```bash
   https://github.com/Z-FranXx/TICKDONE.git

2. Navega al directorio del proyecto:
    ```bash
    cd tickdone

3. Crea un entorno virtual (si no tienes uno):
    ```bash
    python -m venv venv

4.Activa el entorno virtual:

5. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

6. Configura las variables de entorno en un archivo .env:

SECRET_KEY: Clave secreta de Django (puedes generar una nueva con django.core.management.utils.get_random_secret_key()).
DATABASE_URL: La cadena de conexión de tu base de datos PostgreSQL (si usas Render, obtén la URL de la base de datos en el panel de Render).
Realiza las migraciones para crear las tablas en la base de datos:

    ```Bash
    python manage.py migrate

7. Crea un superusuario para acceder al panel de administración de Django:
    ```Bash
    python manage.py createsuperuser
    
8. Inicia el servidor localmente:
    ```Bash
    python manage.py runserver
