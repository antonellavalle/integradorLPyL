from django.shortcuts import get_object_or_404, render, redirect
import requests
from .models import Usuario

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

def artistas(request):
    # Diccionario de géneros con sus respectivos IDs en Deezer
    generos = {
        'rock': 152,
        'pop': 132,
        'electronic': 106,
        'jazz': 129
    }
    
    artistas_por_genero = {}
    
    for genero, genero_id in generos.items():
        # Obtener artistas por género desde Deezer
        artistas_por_genero[genero] = buscar_artistas_por_genero(genero_id)[:10]
    
    return render(request, 'artistas.html', {'artistas_por_genero': artistas_por_genero})

def buscar_artistas_por_genero(genero_id):
    url = f'https://api.deezer.com/genre/{genero_id}/artists'
    response = requests.get(url)
    
    if response.status_code != 200:
        return []  # Retorna una lista vacía si hay un error en la solicitud
    
    data = response.json()
    
    if 'data' in data:
        artistas = [{
            'id': artista['id'],
            'nombre': artista['name'],
            'imagen': artista['picture_medium']
        } for artista in data['data']]
        return artistas[:10]  # Limitamos a los primeros 10 artistas
    else:
        return []
    
import requests
from django.shortcuts import render

def detalle_artista(request, artista_id):
    # URL para obtener la información del artista
    url_artista = f'https://api.deezer.com/artist/{artista_id}'
    response_artista = requests.get(url_artista)
    
    if response_artista.status_code != 200:
        return render(request, 'detalle_artista.html', {'artista': None, 'canciones': []})
    
    # Información del artista
    data_artista = response_artista.json()
    artista = {
        'nombre': data_artista['name'],
        'imagen': data_artista['picture_medium']
    }
    
    # URL para obtener las canciones más populares del artista
    url_canciones = f'https://api.deezer.com/artist/{artista_id}/top'
    response_canciones = requests.get(url_canciones)
    
    if response_canciones.status_code != 200:
        return render(request, 'detalle_artista.html', {'artista': artista, 'canciones': []})
    
    data_canciones = response_canciones.json()
    
    canciones = []
    for track in data_canciones['data']:
        # Convertir la duración de segundos a minutos:segundos
        duracion_segundos = track['duration']
        minutos = duracion_segundos // 60
        segundos = duracion_segundos % 60
        duracion = f"{minutos}:{segundos:02d}"
        
        # Añadir la canción con la imagen del álbum
        canciones.append({
            'titulo': track['title'],
            'id': track['id'],
            'duracion': duracion,
            'imagen': track['album']['cover_medium'],  # URL de la imagen del álbum
            'preview': track['preview']
        })
    
    return render(request, 'detalle_artista.html', {'artista': artista, 'canciones': canciones})


def obtener_canciones_del_artista(artista_id):
    url = f'https://api.deezer.com/artist/{artista_id}/top'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        canciones = [{
            'titulo': track['title'],
            'duracion': track['duration']
        } for track in data['data']]
        return canciones
    else:
        return []
