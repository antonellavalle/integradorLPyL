from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
import requests

class ObtenerAlbumesView(TemplateView):
    template_name = 'albumes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generos = ['pop', 'rock', 'latin', 'metal', 'electronic']
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
        
        context['albumes_por_genero'] = albumes_por_genero
        return context

class ObtenerCancionesDelAlbumView(DetailView):
    template_name = 'canciones.html'
    context_object_name = 'album'

    def get_object(self):
        album_id = self.kwargs.get('album_id')
        url = f'https://api.deezer.com/album/{album_id}'
        response = requests.get(url)
        
        if response.status_code != 200:
            return {}
        
        data = response.json()
        
        return {
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