from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import requests
from ..models import Usuario
from aplicacion.forms import SignUpForm
from django.views import View

def inicio(request):
    return render(request, 'nuevo_inicio.html')

"""
La función signup maneja la creación de un nuevo usuario. Si la solicitud es de tipo POST,
se valida y guarda el usuario. Si los datos son válidos, se crea una instancia del modelo
Usuario asociado con el usuario creado y se redirige al inicio de sesión. Si los datos no 
son válidos, se muestra un mensaje de error. Si la solicitud no es de tipo POST, se muestra
un formulario vacío para el registro de un nuevo usuario.
"""
class RegistroView(View):
    def get(self, request):
        form = SignUpForm()  # Instancia vacía del formulario
        return render(request, 'nuevo_inicio.html', {'form': form, 'signup': True})  # Renderiza la plantilla con el formulario

    def post(self, request):
        form = SignUpForm(request.POST)  # Instancia del formulario con los datos POST
        if form.is_valid():  # Verifica si los datos del formulario son válidos
            user = form.save()  # Guarda el usuario y retorna la instancia del modelo User
            # Crea la instancia del modelo Usuario
            usuario = Usuario.objects.create(
                usuario=user,
                nombre=user.first_name,
                apellido=user.last_name,
                correo=user.email
            )
            messages.success(request, 'Usuario creado correctamente. Ahora puedes iniciar sesión.')  # Mensaje de éxito
            return redirect('iniciar_sesion')  # Redirige a la vista de inicio de sesión
        else:
            # Si el formulario no es válido, mostrar los errores específicos de cada campo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            # Renderiza la plantilla con el formulario y los errores
            return render(request, 'nuevo_inicio.html', {'form': form, 'signup': True})
# Si el formulario no es válido, muestra un mensaje de error

"""
La función iniciar_sesion maneja el proceso de inicio de sesión de un usuario. Si la solicitud es de tipo POST,
se valida el formulario de autenticación. Si los datos son válidos, se autentica al usuario y se inicia la sesión.
Si los datos no son válidos o la autenticación falla, se muestra un mensaje de error. Si la solicitud no es de tipo POST,
se muestra un formulario vacío para el inicio de sesión.
"""
def iniciar_sesion(request):
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        form = AuthenticationForm(data=request.POST)  # Crea una instancia del formulario de autenticación con los datos de la solicitud POST
        
        if form.is_valid():  # Verifica si los datos del formulario son válidos
            username = form.cleaned_data.get('username')  # Obtiene el nombre de usuario del formulario limpio
            password = form.cleaned_data.get('password')  # Obtiene la contraseña del formulario limpio
            
            user = authenticate(username=username, password=password)  # Autentica al usuario con el nombre de usuario y la contraseña
            if user is not None:
                login(request, user)  # Inicia sesión del usuario
                return redirect('principal')  # Redirige al usuario a la vista principal
            else:
                messages.error(request, "Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")  # Muestra un mensaje de error si la autenticación falla
        else:
            messages.error(request, "Error en el formulario de inicio de sesión.")  # Muestra un mensaje de error si el formulario no es válido
    else:
        form = AuthenticationForm()  # Si la solicitud no es de tipo POST, crea una instancia vacía del formulario de autenticación
    
    return render(request, 'nuevo_inicio.html', {'form': form, 'signup': False})  # Renderiza la plantilla nuevo_inicio.html con el formulario y una variable signup