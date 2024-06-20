from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests

# Servicio de Deezer
class DeezerService:
    BASE_URL = "https://api.deezer.com"

    @staticmethod
    def buscar_canciones(query):
        """
        Busca canciones en la API de Deezer utilizando el parámetro de consulta proporcionado.
        """
        url = f"{DeezerService.BASE_URL}/search/track?q={query}"
        response = requests.get(url)

        if response.status_code != 200:
            return None, response.status_code

        data = response.json()
        canciones = []
        if 'data' in data:
            canciones = [{
                'id': cancion.get('id', ''),
                'titulo': cancion.get('title', 'Título no disponible'),
                'artista': cancion.get('artist', {}).get('name', 'Artista no disponible'),
                'imagen': cancion.get('album', {}).get('cover_medium', 'default_cover.jpg'),
                'duracion': DeezerService.formato_duracion(cancion.get('duration', 0))
            } for cancion in data['data']]
        return canciones, None

    @staticmethod
    def formato_duracion(segundos):
        """
        Convierte una duración en segundos al formato mm:ss.
        """
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos}:{segundos:02d}"


# Vista para agregar canciones desde la API de Deezer
class AgregarCancionesView(View):
    def get(self, request):
        """
        Maneja la solicitud GET para buscar canciones en la API de Deezer según la consulta proporcionada.
        """
        query = request.GET.get('query', '')
        canciones, error = DeezerService.buscar_canciones(query)
        
        if error:
            return JsonResponse({'error': 'Error al consultar la API de Deezer'}, status=error)

        return JsonResponse(canciones, safe=False)


# Vista para listar las listas de reproducción
class ListarReproduccionView(View):
    def get(self, request):
        """
        Renderiza la plantilla de listas de reproducción.
        """
        return render(request, 'listasReproducion.html')
