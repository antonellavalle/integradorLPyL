from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from aplicacion.models import ListaReproduccion, Cancion, Artista
import json
import requests


class ListasReproduccionView(LoginRequiredMixin, View):
    def get(self, request):
        listas = ListaReproduccion.objects.filter(usuario=request.user)
        return render(request, 'listasReproduccion.html', {'listas': listas})

    def post(self, request):
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'crear_lista':
            nombre = data.get('nombre')
            lista = ListaReproduccion.objects.create(nombre=nombre, usuario=request.user)
            return JsonResponse({'id': lista.id, 'nombre': lista.nombre})

        elif action == 'agregar_cancion':
            lista_id = data.get('lista_id')
            cancion_data = data.get('cancion')
            lista = ListaReproduccion.objects.get(id=lista_id, usuario=request.user)
            cancion, created = Cancion.objects.get_or_create(
                titulo=cancion_data['titulo'],
                artista=cancion_data['artista'],
                defaults={'album': None, 'duracion': cancion_data['duracion']}
            )
            lista.canciones.add(cancion)
            return JsonResponse({'success': True})

        elif action == 'eliminar_cancion':
            lista_id = data.get('lista_id')
            cancion_id = data.get('cancion_id')
            lista = ListaReproduccion.objects.get(id=lista_id, usuario=request.user)
            cancion = Cancion.objects.get(id=cancion_id)
            lista.canciones.remove(cancion)
            return JsonResponse({'success': True})

        elif action == 'eliminar_lista':
            lista_id = data.get('lista_id')
            ListaReproduccion.objects.filter(id=lista_id, usuario=request.user).delete()
            return JsonResponse({'success': True})

        return JsonResponse({'error': 'Acción no válida'}, status=400)

class AgregarCancionesView(View):
    def get(self, request):
        """ Maneja la búsqueda de canciones """
        query = request.GET.get('query', '')
        # Aquí puedes implementar la lógica para buscar canciones en la API de Deezer
        # Por ahora, usaremos un ejemplo simplificado
        response = requests.get(f'https://api.deezer.com/search?q={query}&limit=10')
        if response.status_code == 200:
            canciones = response.json().get('data', [])
            resultados = [
                {
                    'id': cancion['id'],
                    'titulo': cancion['title'],
                    'artista': cancion['artist']['name'],
                    'duracion': cancion['duration'],
                    'imagen': cancion['album']['cover_medium']
                }
                for cancion in canciones
            ]
            return JsonResponse(resultados, safe=False)
        else:
            return JsonResponse({'error': 'No se pudo realizar la búsqueda'}, status=400)

    def post(self, request):
        """ Maneja la adición de canciones a la lista de reproducción """
        data = json.loads(request.body)
        lista_id = data.get('lista_id')
        cancion_data = data.get('cancion')
        
        try:
            lista = ListaReproduccion.objects.get(id=lista_id, usuario=request.user)
            artista, _ = Artista.objects.get_or_create(nombre=cancion_data['artista'])
            cancion, created = Cancion.objects.get_or_create(
                titulo=cancion_data['titulo'],
                artista=artista,
                defaults={'duracion': cancion_data['duracion']}
            )
            lista.canciones.add(cancion)
            return JsonResponse({'success': True})
        except ListaReproduccion.DoesNotExist:
            return JsonResponse({'error': 'Lista de reproducción no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)