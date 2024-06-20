
from django.shortcuts import render
import requests


def obtener_albumes(request):
    generos = ['pop', 'rock', 'latin', 'metal', 'electronic']  # Añade más géneros según sea necesario
    albumes_por_genero = {}
    
    for genero in generos:
        url = 'https://api.deezer.com/search/album'
        params = {
            'q': genero,
            'limit': 10
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                albumes_por_genero[genero] = [{
                    'id': album['id'],
                    'titulo': album['title'],
                    'artista': album['artist']['name'],
                    'imagen': album['cover_medium'],
                } for album in data['data']]
    
    return render(request, 'albumes.html', {'albumes_por_genero': albumes_por_genero})

def obtener_canciones_del_album(request, album_id):
    url = f'https://api.deezer.com/album/{album_id}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return render(request, 'canciones.html', {'canciones': [], 'album': {}})
    
    data = response.json()
    
    album = {
        'titulo': data['title'],
        'artista': data['artist']['name'],
        'imagen': data['cover_medium'],
        'canciones': [{
            'titulo': track['title'],
            'duracion': track['duration'],
            'duracion_formatted': f"{track['duration'] // 60}:{track['duration'] % 60:02d}",
            'id': track['id']
        } for track in data['tracks']['data']]
    }
    
    return render(request, 'canciones.html', {'album': album})