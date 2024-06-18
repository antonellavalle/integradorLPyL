from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import requests
from .models import Usuario
from aplicacion.forms import SignUpForm

def inicio(request):
    return render(request, 'nuevo_inicio.html')

"""
La función signup maneja la creación de un nuevo usuario. Si la solicitud es de tipo POST,
se valida y guarda el usuario. Si los datos son válidos, se crea una instancia del modelo
Usuario asociado con el usuario creado y se redirige al inicio de sesión. Si los datos no 
son válidos, se muestra un mensaje de error. Si la solicitud no es de tipo POST, se muestra
un formulario vacío para el registro de un nuevo usuario.
"""
def signup(request):
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
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
    else:
        form = SignUpForm()  # Si la solicitud no es de tipo POST, crea una instancia vacía del formulario SignUpForm
    return render(request, 'nuevo_inicio.html', {'form': form, 'signup': True})  # Renderiza la plantilla nuevo_inicio.html con el formulario y una variable signup

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

"""
La función principal renderiza la vista principal de la aplicación.
"""
def principal(request):
    cancionesTrap = obtener_canciones_de_genero('trap')
    cancionesRock = obtener_canciones_de_genero('rock')
    cancionesTendencia = canciones_en_tendencia()
    lanzamientos = nuevos_lanzamientos_en_arg()
    contexto = {
        'cancionesTrap': cancionesTrap,
        'cancionesRock': cancionesRock,
        'cancionesTendencia': cancionesTendencia,
        'lanzamientos': lanzamientos
    }
    return render(request, 'principal.html', contexto)


def obtener_canciones_de_genero(genero, limite=5):
    url = 'https://api.deezer.com/search'
    params = {
        'q': genero,
        'limit': limite  
    }
    response = requests.get(url, params=params)  # Realiza la solicitud GET a la API de Deezer

    if response.status_code != 200:  # Verifica si la respuesta no tiene un código de estado 200
        return []  # Retorna una lista vacia si hay un error en la solicitud

    data = response.json()  # Convierte la respuesta en formato JSON

    if 'data' in data:
        canciones = [{  # Extrae la información relevante de las canciones
            'id': cancion['id'],
            'titulo': cancion['title'],
            'artista': cancion['artist']['name'],
            'url': cancion['link'],
            'imagen': cancion['album']['cover_medium'],
            'duracion': formato_duracion(cancion['duration'])  
        } for cancion in data['data']]
        return canciones
    else:
        return []  # Retorna una lista vacía si no hay datos de canciones

    





"""
La función buscar_artista maneja la búsqueda de artistas y canciones utilizando la API de Deezer.
Si la solicitud contiene el parámetro 'q', se realizan las búsquedas de artistas y canciones y se 
muestran los resultados.
"""
def buscar_artista(request):
    artistas = []
    canciones = []

    if 'q' in request.GET:  # Verifica si el parámetro 'q' está presente en la solicitud GET
        query = request.GET['q']  # Obtiene el valor del parámetro 'q'
        artistas = buscar_artistas_deezer(query)  # Busca artistas utilizando la API de Deezer
        canciones = buscar_canciones_deezer(query)  # Busca canciones utilizando la API de Deezer

    return render(request, 'buscar_artista.html', {'artistas': artistas, 'canciones': canciones})  # Renderiza la plantilla buscar_artista.html con los resultados

"""
La función buscar_canciones_deezer busca canciones en la API de Deezer según el query proporcionado.
Retorna una lista de canciones con su información relevante.
"""
def buscar_canciones_deezer(query):
    url = f'https://api.deezer.com/search/track?q={query}'  # Construye la URL de la solicitud a la API de Deezer
    response = requests.get(url)  # Realiza la solicitud GET a la API de Deezer
    
    if response.status_code != 200:  # Verifica si la respuesta no tiene un código de estado 200
        return []  # Retorna una lista vacía si hay un error en la solicitud
    
    data = response.json()  # Convierte la respuesta en formato JSON
    
    if 'data' in data:
        canciones = [{  # Extrae y estructura la información relevante de las canciones
            'id': cancion['id'],
            'titulo': cancion['title'],
            'url': cancion['link'],
            'imagen': cancion['album']['cover_medium'],
            'duracion': formato_duracion(cancion['duration'])
        } for cancion in data['data']]
        return canciones
    else:
        return []  # Retorna una lista vacía si no hay datos de canciones

# Usado para poder buscar canciones en las listas de reproducion
def agregar_canciones(request):
    query = request.GET.get('query', '')
    url = f'https://api.deezer.com/search/track?q={query}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return JsonResponse({'error': 'Error al consultar la API de Deezer'}, status=response.status_code)
    
    data = response.json()
    
    canciones = []
    if 'data' in data:
        canciones = [{
            'id': cancion.get('id', ''),
            'titulo': cancion.get('title', 'Título no disponible'),
            'artista': cancion.get('artist', {}).get('name', 'Artista no disponible'),
            'imagen': cancion.get('album', {}).get('cover_medium', 'default_cover.jpg'),
            'duracion': formato_duracion(cancion.get('duration', 0))
        } for cancion in data['data']]
    
    return JsonResponse(canciones, safe=False)
# Usado para poder buscar canciones en las listas de reproducion

"""
La función obtener_canciones obtiene las canciones de un artista específico utilizando la API de Deezer.
"""
def obtener_canciones(request, artista_id):
    canciones = obtener_canciones_de_deezer(artista_id)  # Obtiene las canciones del artista
    return render(request, 'obtener_canciones.html', {'canciones': canciones})  # Renderiza la plantilla obtener_canciones.html con los resultados

"""
La función buscar_artistas_deezer busca artistas en la API de Deezer según el query proporcionado.
Retorna una lista de artistas con su información relevante.
"""
def buscar_artistas_deezer(query):
    url = f'https://api.deezer.com/search/artist?q={query}'  # Construye la URL de la solicitud a la API de Deezer
    response = requests.get(url)  # Realiza la solicitud GET a la API de Deezer
    
    if response.status_code != 200:  # Verifica si la respuesta no tiene un código de estado 200
        return []  # Retorna una lista vacía si hay un error en la solicitud
    
    data = response.json()  # Convierte la respuesta en formato JSON
    
    if 'data' in data:
        artistas = [{  # Extrae y estructura la información relevante de los artistas
            'id': artista['id'],
            'nombre': artista['name'],
            'imagen': artista['picture_medium']
        } for artista in data['data']]
        return artistas
    else:
        return []  # Retorna una lista vacía si no hay datos de artistas

"""
La función formato_duracion convierte una duración en segundos en un formato de minutos y segundos.
"""
def formato_duracion(segundos):
    minutos = segundos // 60  # Calcula los minutos
    segundos = segundos % 60  # Calcula los segundos restantes
    return f"{minutos}:{segundos:02d}"  # Retorna la duración en formato mm:ss

"""
La función obtener_canciones_de_deezer obtiene las canciones más populares de un artista utilizando la API de Deezer.
Retorna una lista de canciones con su información relevante.
"""
def obtener_canciones_de_deezer(artista_id):
    url = f'https://api.deezer.com/artist/{artista_id}/top?limit=10'  # Construye la URL de la solicitud a la API de Deezer
    response = requests.get(url)  # Realiza la solicitud GET a la API de Deezer
    
    if response.status_code != 200:  # Verifica si la respuesta no tiene un código de estado 200
        return []  # Retorna una lista vacía si hay un error en la solicitud
    
    data = response.json()  # Convierte la respuesta en formato JSON
    
    if 'data' in data:
        canciones = [{  # Extrae y estructura la información relevante de las canciones
            'id': cancion['id'],
            'titulo': cancion['title'],
            'url': cancion['link'],
            'imagen': cancion['album']['cover_medium'],  # Incluye la URL de la imagen de la carátula
            'duracion': formato_duracion(cancion['duration'])  # Incluye la duración de la canción en segundos
        } for cancion in data['data']]
        return canciones
    else:
        return []  # Retorna una lista vacía si no hay datos de canciones

"""
La función canciones_en_tendencia obtiene las canciones en tendencia utilizando la API de Deezer y las retorna en formato JSON.
"""


def canciones_en_tendencia():
    url = 'https://api.deezer.com/chart/0/tracks?limit=5&country=ar'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        canciones = []

        for cancion in data['data']:
            info_cancion = {
                'titulo': cancion['title'],
                'artista': cancion['artist']['name'],
                'album': cancion['album']['title'],
                'imagen': cancion['album']['cover_medium'],
                'duracion': formato_duracion(cancion['duration']),
            }
            canciones.append(info_cancion)

        return canciones  # Devuelve la lista de canciones en forma de lista de diccionarios
    else:
        return []  # En caso de error, devuelve una lista vacía o maneja el error según necesites


def nuevos_lanzamientos_en_arg():
    print("Se ha recibido una solicitud para la vista nuevos_lanzamientos_en_arg.")
    url = "https://api.deezer.com/editorial/0/releases?limit=5&country=ar"

    response = requests.get(url)

    if response.status_code == 200:
        print("La API está respondiendo correctamente.")
        data = response.json()
        print("Datos recibidos:", data)
        
        # Extraer la información relevante de la respuesta
        lanzamientos = []
        for cancion in data.get('data', []):
            titulo = cancion.get('title', 'Sin título')
            artista = cancion.get('artist', {}).get('name', 'Desconocido')
            imagen = cancion.get('cover_medium', '') 
            duracion = cancion.get('duration', None)  # Usar None si no está disponible
            print("Duración de la canción:", duracion) 

            info_cancion = {
                'titulo': titulo,
                'artista': artista,
                'imagen': imagen,
                'duracion': formato_duracion(duracion) if duracion else 'Desconocida',  # Mostrar 'Desconocida' si no está disponible
            }
            lanzamientos.append(info_cancion)

        # Retornar los datos como lista de diccionarios
        return lanzamientos
    else:
        # En caso de error, devuelve una lista vacía
        return []

"""
La función listar_usuarios muestra una lista de todos los usuarios registrados.
"""
def listar_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})  # Renderiza la plantilla listar_usuarios.html con la lista de usuarios

"""
La función detalle_usuario muestra los detalles de un usuario específico.
"""
def detalle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)  # Obtiene el usuario específico o retorna un 404 si no existe
    return render(request, 'detalle_usuario.html', {'usuario': usuario})  # Renderiza la plantilla detalle_usuario.html con los detalles del usuario

"""
La función editar_usuario maneja la edición de los datos de un usuario específico.
"""
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)  # Obtiene el usuario específico o retorna un 404 si no existe
    
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        # Aquí iría la lógica para editar el usuario
        return redirect('detalle_usuario', pk=pk)  # Redirige a la vista de detalles del usuario después de editarlo
    else:
        return render(request, 'editar_usuario.html', {'usuario': usuario})  # Renderiza la plantilla editar_usuario.html con los datos del usuario

"""
La función eliminar_usuario maneja la eliminación de un usuario específico.
"""
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)  # Obtiene el usuario específico o retorna un 404 si no existe
    
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        # Aquí iría la lógica para eliminar el usuario
        return redirect('listar_usuarios')  # Redirige a la vista de lista de usuarios después de eliminarlo
    else:
        return render(request, 'eliminar_usuario.html', {'usuario': usuario})  # Renderiza la plantilla eliminar_usuario.html con los datos del usuario

def listas_de_reproducion(request):
    return render(request, 'listasReproducion.html')
