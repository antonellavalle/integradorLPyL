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

def signup(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Imprime los datos recibidos

        form = SignUpForm(request.POST)
        
        if form.is_valid():
            print("Form is valid")
            
            user = form.save()  # Aquí se usa el método save del formulario
            
            usuario = Usuario.objects.create(
                usuario=user,
                nombre=user.first_name,
                apellido=user.last_name,
                correo=user.email
            )
            
            messages.success(request, "Usuario creado correctamente. Ahora puedes iniciar sesión.")
            return redirect('iniciar_sesion')
        else:
            print("Form errors:", form.errors)  # Imprime los errores del formulario
            for field, errors in form.errors.items():
                print(f"Error in {field}: {errors}")
            messages.error(request, "Error al registrarse. Verifique los datos ingresados.")
    else:
        form = SignUpForm()
    
    return render(request, 'nuevo_inicio.html', {'form': form, 'signup': True})


'''def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Usuario = Usuario.objects.create(
                usuario=user.first_name,
                nombre=user.first_name,
                apellido=user.last_name,
                correo=user.email
            )
            messages.success(request, "Usuario creado correctamente. Ahora puedes iniciar sesión.")
            return redirect('iniciar_sesion')
        else:
            messages.error(request, "Error al registrarse. Verifique los datos ingresados.")
    else:
        form = SignUpForm()
    return render(request, 'nuevo_inicio.html', {'form': form, 'signup': True})
'''
def iniciar_sesion(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Imprime los datos recibidos

        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            print("Form is valid")
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Cleaned data - Email: {username}, Password: {password}")
            
            user = authenticate(username=username, password=password)
            if user is not None:
                print("Authentication successful")
                login(request, user)
                return redirect('principal')
            else:
                print("Authentication failed")
                messages.error(request, "Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        else:
            print("Form errors:", form.errors)  # Imprime los errores del formulario
            messages.error(request, "Error en el formulario de inicio de sesión.")
    else:
        print("GET request received")
        form = AuthenticationForm()
    
    return render(request, 'nuevo_inicio.html', {'form': form, 'signup': False})


'''def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('principal')
            else:
                messages.error(request, "Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        else:
            messages.error(request, "Error en el formulario de inicio de sesión.")
    else:
        form = AuthenticationForm()
    return render(request, 'nuevo_inicio.html', {'form': form, 'signup': False})
'''
def principal(request):
    return render(request, 'principal.html')
 
def buscar_artista(request):
    artistas = []
    canciones = []

    if 'q' in request.GET:
        query = request.GET['q']
        artistas = buscar_artistas_deezer(query)
        canciones = buscar_canciones_deezer(query)

    return render(request, 'buscar_artista.html', {'artistas': artistas, 'canciones': canciones})


def buscar_canciones_deezer(query):
    url = f'https://api.deezer.com/search/track?q={query}'
    response = requests.get(url)
    print(f'Solicitando canciones con query: {query}')
    print(f'Respuesta de la API de Deezer: {response}')
    
    if response.status_code != 200:
        print('Error en la solicitud a Deezer')
        return []
    
    data = response.json()
    print(f'Datos recibidos: {data}')
    
    if 'data' in data:
        canciones = [{
            'id': cancion['id'],
            'titulo': cancion['title'],
            'url': cancion['link'],
            'imagen': cancion['album']['cover_medium'],
            'duracion': formato_duracion(cancion['duration'])
        } for cancion in data['data']]
        return canciones
    else:
        return []


def obtener_canciones(request, artista_id):
    canciones = obtener_canciones_de_deezer(artista_id)
    return render(request, 'obtener_canciones.html', {'canciones': canciones})

def buscar_artistas_deezer(query):
    url = f'https://api.deezer.com/search/artist?q={query}'
    response = requests.get(url)
    print(f'Solicitando artistas con query: {query}')
    print(f'Respuesta de la API de Deezer: {response}')
    
    if response.status_code != 200:
        print('Error en la solicitud a Deezer')
        return []
    
    data = response.json()
    print(f'Datos recibidos: {data}')
    
    if 'data' in data:
        artistas = [{'id': artista['id'], 'nombre': artista['name'], 'imagen': artista['picture_medium']} for artista in data['data']]
        return artistas
    else:
        return []

def formato_duracion(segundos):
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos}:{segundos:02d}"


def obtener_canciones_de_deezer(artista_id):
    url = f'https://api.deezer.com/artist/{artista_id}/top?limit=10'
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    if 'data' in data:
        canciones = [{
            'id': cancion['id'],
            'titulo': cancion['title'],
            'url': cancion['link'],
            'imagen': cancion['album']['cover_medium'],  # Incluye la URL de la imagen de la carátula
            'duracion': formato_duracion(cancion['duration'])  # Incluye la duración de la canción en segundos
        } for cancion in data['data']]
        return canciones
    else:
        return []
    
def canciones_en_tendencia(request):
    print("Se ha recibido una solicitud para la vista canciones_en_tendencia.")
    url = 'https://api.deezer.com/chart/0/tracks?limit=5&country=ar'
    response = requests.get(url)

    if response.status_code == 200:
        print("La API está respondiendo correctamente.")
        data = response.json()
        print("Datos recibidos:", data)
        
        # Extraer la información relevante de la respuesta
        canciones = []
        for cancion in data['data']:
            info_cancion = {
                'titulo': cancion['title'],
                'artista': cancion['artist']['name'],
                'album': cancion['album']['title'],
                'imagen': cancion['album']['cover_medium'],  # Aca se obtiene la URL de la imagen directamente de la API
                 'duracion':  formato_duracion(cancion['duration']),  # Agregamos la duración de la canción
            }
            canciones.append(info_cancion)

        # Retornar los datos como respuesta JSON
        return JsonResponse({'canciones': canciones})
    else:
        print("Hubo un problema al hacer la solicitud a la API. Código de estado:", response.status_code)
        # Si hay un error en la solicitud a la API, devuelve un mensaje de error
        return JsonResponse({'error': 'Hubo un problema al hacer la solicitud a la API'}, status=500)

    '''Modifico desde aca '''
    

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

def detalle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'detalle_usuario.html', {'usuario': usuario})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        # Aquí iría la lógica para editar el usuario
        return redirect('detalle_usuario', pk=pk)
    else:
        return render(request, 'editar_usuario.html', {'usuario': usuario})

def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        # Aquí iría la lógica para eliminar el usuario
        return redirect('listar_usuarios')
    else:
        return render(request, 'eliminar_usuario.html', {'usuario': usuario})
'''
def buscar_artistas_en_musicbrainz(query):
    # Realiza una solicitud a la API de MusicBrainz para buscar artistas que coincidan con el query
    url = f'http://musicbrainz.org/ws/2/artist/?query={query}&fmt=json'
    response = requests.get(url)
    data = response.json()
    
    # Verifica si se recibieron datos correctamente
    if 'artists' in data:
        # Extrae los artistas de los datos recibidos
        artistas = [{'id': artista['id'], 'nombre': artista['name']} for artista in data['artists']]
        return artistas
    else:
        # Si no se reciben datos o hay un error, retorna una lista vacía
        return []

def buscar_artista(request):
    artistas = []
    if 'q' in request.GET:
        query = request.GET['q']
        artistas = buscar_artistas_en_musicbrainz(query)
    return render(request, 'buscar_artista.html', {'artistas': artistas})


def obtener_canciones_de_musicbrainz(artista_id):
    print(f'Solicitando canciones para el artista con ID: {artista_id}')
    # Realiza una solicitud a la API de MusicBrainz para obtener información del artista y sus grabaciones
    url = f'http://musicbrainz.org/ws/2/artist/{artista_id}?inc=recordings&fmt=json'
    response = requests.get(url)
    print(f'Respuesta de la API de MusicBrainz: {response}')
    
    # Verifica si se recibieron datos correctamente
    if response.status_code == 200:
        data = response.json()
        print(f'Datos recibidos: {data}')
        
        if 'recordings' in data:
            # Extrae las grabaciones (canciones) del artista de los datos recibidos
            canciones = [{'id': grabacion['id'], 'titulo': grabacion['title']} for grabacion in data['recordings']]
            print(f'Canciones obtenidas: {canciones}')
            return canciones
        else:
            # Si no se reciben datos de grabaciones, retorna una lista vacía
            print('No se encontraron grabaciones para este artista.')
            return []
    else:
        # Si no se recibe una respuesta exitosa, muestra un mensaje de error y retorna una lista vacía
        print(f'Error al solicitar datos: {response.status_code}')
        return []


def obtener_canciones(request, artista_id):
    # Aquí deberías agregar la lógica para obtener las canciones del artista con el ID proporcionado
    canciones = obtener_canciones_de_musicbrainz(artista_id)
    return render(request, 'obtener_canciones.html', {'canciones': canciones})
'''

