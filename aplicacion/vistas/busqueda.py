import requests
from django.shortcuts import render

class DeezerAPI:
    @staticmethod
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
                'imagen': cancion['album']['cover_medium'],
                'duracion': DeezerAPI.formato_duracion(cancion['duration'])
            } for cancion in data['data']]
            return canciones
        else:
            return []
    
    @staticmethod
    def obtener_canciones_de_genero(genero, limite=5):
        url = 'https://api.deezer.com/search'
        params = {
            'q': genero,
            'limit': limite
        }
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        
        if 'data' in data:
            canciones = [{
                'id': cancion['id'],
                'titulo': cancion['title'],
                'artista': cancion['artist']['name'],
                'url': cancion['link'],
                'imagen': cancion['album']['cover_medium'],
                'duracion': DeezerAPI.formato_duracion(cancion['duration'])
            } for cancion in data['data']]
            return canciones
        else:
            return []

    @staticmethod
    def buscar_canciones_deezer(query):
        url = f'https://api.deezer.com/search/track?q={query}'
        response = requests.get(url)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        
        if 'data' in data:
            canciones = [{
                'id': cancion['id'],
                'titulo': cancion['title'],
                'url': cancion['link'],
                'imagen': cancion['album']['cover_medium'],
                'duracion': DeezerAPI.formato_duracion(cancion['duration'])
            } for cancion in data['data']]
            return canciones
        else:
            return []

    @staticmethod
    def buscar_artistas_deezer(query):
        url = f'https://api.deezer.com/search/artist?q={query}'
        response = requests.get(url)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        
        if 'data' in data:
            artistas = [{
                'id': artista['id'],
                'nombre': artista['name'],
                'imagen': artista['picture_medium']
            } for artista in data['data']]
            return artistas
        else:
            return []

    @staticmethod
    def formato_duracion(segundos):
        # Función para formatear la duración de la canción (puede implementarse según necesidades)
        # Por ejemplo, para devolver un string formateado de tiempo
        return f'{segundos // 60}:{segundos % 60:02}'

def buscar_artista(request):
    artistas = []
    canciones = []

    if 'q' in request.GET:
        query = request.GET['q']
        artistas = DeezerAPI.buscar_artistas_deezer(query)
        canciones = DeezerAPI.buscar_canciones_deezer(query)

    return render(request, 'buscar_artista.html', {'artistas': artistas, 'canciones': canciones})

def obtener_canciones(request, artista_id):
    canciones = DeezerAPI.obtener_canciones_de_deezer(artista_id)
    return render(request, 'obtener_canciones.html', {'canciones': canciones})
