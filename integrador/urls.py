from django.contrib import admin
from django.urls import path
from aplicacion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base,name='base'),
    path('', views.inicio, name='inicio'),
    path('signup/', views.signup, name='signup'),#aca viene mi registro
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('principal/', views.principal, name='principal'),
    path('buscar/', views.buscar_artista, name='buscar_artista'),
    path('canciones/<str:artista_id>/', views.obtener_canciones, name='obtener_canciones'),
    path('canciones_en_tendencia/', views.canciones_en_tendencia, name='canciones_en_tendencia'),
    path('nuevos_lanzamientos_en_arg/', views.nuevos_lanzamientos_en_arg, name='nuevos_lanzamientos_en_arg'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
]

