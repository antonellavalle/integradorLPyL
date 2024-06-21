from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests

# === Vistas para las Listas de Reproducción ===

class ListasReproduccionView(View):
    """
    Muestra la página principal de las listas de reproducción.
    """

    def get(self, request):
        """
        Renderiza la plantilla para las listas de reproducción.
        """
        return render(request, 'listasReproducion.html')


class AgregarCancionesView(View):
    """
    Maneja la búsqueda y el agregado de canciones desde la API de Deezer.
    """

    def get(self, request):
        """
        Procesa la búsqueda de canciones usando la API de Deezer y retorna los resultados en formato JSON.
        """
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
                'duracion': self.formato_duracion(cancion.get('duration', 0))
            } for cancion in data['data']]

        return JsonResponse(canciones, safe=False)

    def formato_duracion(self, segundos):
        """
        Convierte la duración en segundos a un formato mm:ss.
        """
        minutos = segundos // 60
        segundos_restantes = segundos % 60
        return f'{minutos:02}:{segundos_restantes:02}'
