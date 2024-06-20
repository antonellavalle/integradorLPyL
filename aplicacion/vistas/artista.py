import requests
from django.shortcuts import render
from django.views import View

class DeezerService:
    BASE_URL = "https://api.deezer.com"
    
    @staticmethod
    def obtener_artistas_por_genero(genero_id, limite=10):
        """Obtiene una lista de artistas por género."""
        url = f"{DeezerService.BASE_URL}/genre/{genero_id}/artists"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('data', [])
            return [{
                'id': artista['id'],
                'nombre': artista['name'],
                'imagen': artista['picture_medium']
            } for artista in data[:limite]]
        return []

    @staticmethod
    def obtener_detalle_artista(artista_id):
        """Obtiene la información detallada de un artista."""
        url = f"{DeezerService.BASE_URL}/artist/{artista_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def obtener_canciones_del_artista(artista_id, limite=10):
        """Obtiene las canciones más populares de un artista."""
        url = f"{DeezerService.BASE_URL}/artist/{artista_id}/top"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('data', [])
            canciones = []
            for track in data[:limite]:
                duracion_segundos = track['duration']
                minutos = duracion_segundos // 60
                segundos = duracion_segundos % 60
                duracion = f"{minutos}:{segundos:02d}"
                canciones.append({
                    'titulo': track['title'],
                    'id': track['id'],
                    'duracion': duracion,
                    'imagen': track['album']['cover_medium'],
                    'preview': track['preview']
                })
            return canciones
        return []

class ArtistaListView(View):
    """Vista para mostrar artistas por género."""
    def get(self, request):
        generos = {
            'rock': 152,
            'pop': 132,
            'electronic': 106,
            'jazz': 129
        }
        artistas_por_genero = {}
        
        for genero, genero_id in generos.items():
            artistas_por_genero[genero] = DeezerService.obtener_artistas_por_genero(genero_id)
        
        return render(request, 'artistas.html', {'artistas_por_genero': artistas_por_genero})

class ArtistaDetailView(View):
    """Vista para mostrar los detalles de un artista y sus canciones más populares."""
    def get(self, request, artista_id):
        artista_info = DeezerService.obtener_detalle_artista(artista_id)
        if not artista_info:
            return render(request, 'detalle_artista.html', {'artista': None, 'canciones': []})
        
        canciones = DeezerService.obtener_canciones_del_artista(artista_id)
        artista = {
            'nombre': artista_info['name'],
            'imagen': artista_info['picture_medium']
        }
        
        return render(request, 'detalle_artista.html', {'artista': artista, 'canciones': canciones})
