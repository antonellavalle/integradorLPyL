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
        form = SignUpForm()  # Si la solicitud no es de tipo POST, crea una instancia vacía del formulario SignUpForm
        return render(request, 'nuevo_inicio.html', {'form': form, 'signup': True})  # Renderiza la plantilla nuevo_inicio.html con el formulario y una variable signup
    
    def post(self, request):
        form = SignUpForm(request.POST)  # Crea una instancia del formulario SignUpForm con los datos de la solicitud POST
        if form.is_valid():  # Verifica si los datos del formulario son válidos
            user = form.save()  # Guarda la instancia del modelo User utilizando el método save del formulario
            usuario = Usuario.objects.create(  # Crea una instancia del modelo Usuario asociada con el usuario creado
                usuario=user,  # Asigna la instancia del modelo User al campo usuario
                nombre=user.first_name,  # Asigna el primer nombre del usuario
                apellido=user.last_name,  # Asigna el apellido del usuario
                correo=user.email  # Asigna el correo electrónico del usuario
            )
            messages.success(request, "Usuario creado correctamente. Ahora puedes iniciar sesión.")  # Muestra un mensaje de éxito indicando que el usuario se creó correctamente
            return redirect('iniciar_sesion')  # Redirige al usuario a la vista de inicio de sesión
        else:
            messages.error(request, "Error al registrarse. Verifique los datos ingresados.")  # Si el formulario no es válido, muestra un mensaje de error

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