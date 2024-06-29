from django.contrib import admin
from django.urls import path
from aplicacion import views
from aplicacion.vistas.login import RegistroView, iniciar_sesion, cerrar_sesion, inicio
from aplicacion.vistas.album import obtener_albumes, obtener_canciones_del_album
from aplicacion.vistas.artista import ArtistaListView, ArtistaDetailView
from aplicacion.vistas.lista_reproduccion import ListasReproduccionView, AgregarCancionesView
from aplicacion.vistas.busqueda import buscar_artista, obtener_canciones
from aplicacion.vistas.principal import principal, canciones_en_tendencia, nuevos_lanzamientos_en_arg
from aplicacion.vistas.usuario import UserUpdateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('signup/', RegistroView.as_view(), name='signup'),
    path('login/', iniciar_sesion, name='iniciar_sesion'),
    path('principal/', principal, name='principal'),
    path('buscar/', buscar_artista, name='buscar_artista'),
    path('canciones/<str:artista_id>/', obtener_canciones, name='obtener_canciones'),
    path('canciones_en_tendencia/', canciones_en_tendencia, name='canciones_en_tendencia'),
    path('nuevos_lanzamientos_en_arg/', nuevos_lanzamientos_en_arg, name='nuevos_lanzamientos_en_arg'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('listas/', ListasReproduccionView.as_view(), name='listas_de_reproduccion'),
    path('agregar_canciones/', AgregarCancionesView.as_view(), name='agregar_canciones'),
    path('artistas/', ArtistaListView.as_view(), name='artistas'),
    path('artista/<int:artista_id>/', ArtistaDetailView.as_view(), name='detalle_artista'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('albumes/', obtener_albumes, name='albumes'),
    path('albumes/<int:album_id>/', obtener_canciones_del_album, name='canciones_del_album'),
    path('editar_usuario/', UserUpdateView.as_view(), name='editar_usuario'),

]

