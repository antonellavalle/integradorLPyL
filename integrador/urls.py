from django.contrib import admin
from django.urls import path
from aplicacion import views
from aplicacion.vistas.login import RegistroView, inicio, iniciar_sesion
from aplicacion.vistas.album import obtener_albumes, obtener_canciones_del_album

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('signup/', RegistroView.as_view(), name='signup'),#aca viene mi registro
    path('login/', iniciar_sesion, name='iniciar_sesion'),
    path('principal/', views.principal, name='principal'),
    path('buscar/', views.buscar_artista, name='buscar_artista'),
    path('canciones/<str:artista_id>/', views.obtener_canciones, name='obtener_canciones'),
    path('canciones_en_tendencia/', views.canciones_en_tendencia, name='canciones_en_tendencia'),
    path('nuevos_lanzamientos_en_arg/', views.nuevos_lanzamientos_en_arg, name='nuevos_lanzamientos_en_arg'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('listas/', views.listas_de_reproducion,name='listas'),
    path('agregar_canciones/', views.agregar_canciones, name='agregar_canciones'), # Usado para poder buscar canciones en las listas de reproducion
    path('artistas/', views.artistas, name='artistas'),
    path('artista/<int:artista_id>/', views.detalle_artista, name='detalle_artista'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('albumes/', obtener_albumes, name='albumes'),
    path('albumes/<int:album_id>/', obtener_canciones_del_album, name='canciones_del_album'),
]

