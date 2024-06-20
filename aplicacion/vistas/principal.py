# aplicacion/vistas/principal.py
from django.shortcuts import render
from aplicacion.vistas.busqueda import DeezerAPI
import requests

def principal(request):
    cancionesTrap = DeezerAPI.obtener_canciones_de_genero('trap')   
    cancionesRock = DeezerAPI.obtener_canciones_de_genero('rock')

    cancionesTendencia = canciones_en_tendencia()
    lanzamientos = nuevos_lanzamientos_en_arg()
    
    contexto = {
        'cancionesTrap': cancionesTrap,
        'cancionesRock': cancionesRock,
        'cancionesTendencia': cancionesTendencia,
        'lanzamientos': lanzamientos
    }
    return render(request, 'principal.html', contexto)

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
                'duracion': DeezerAPI.formato_duracion(cancion['duration']),
            }
            canciones.append(info_cancion)
        
        return canciones
    else:
        return []

def nuevos_lanzamientos_en_arg():
    url = "https://api.deezer.com/editorial/0/releases?limit=5&country=ar"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        lanzamientos = []
        
        for cancion in data.get('data', []):
            titulo = cancion.get('title', 'Sin título')
            artista = cancion.get('artist', {}).get('name', 'Desconocido')
            imagen = cancion.get('cover_medium', '') 
            duracion = cancion.get('duration', None)
            
            info_cancion = {
                'titulo': titulo,
                'artista': artista,
                'imagen': imagen,
                'duracion': DeezerAPI.formato_duracion(duracion) if duracion else 'Desconocida',
            }
            lanzamientos.append(info_cancion)
        
        return lanzamientos
    else:
        return []
