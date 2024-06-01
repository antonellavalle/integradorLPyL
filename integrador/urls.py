"""
URL configuration for integrador project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from aplicacion import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('registro/', views.signup,name='registro'),
    path('principal/',views.principal,name='principal'),
    path('buscar/', views.buscar_artista,name='buscar_artista'),
    path('canciones/<str:artista_id>/', views.obtener_canciones, name='obtener_canciones'),
    path('canciones_en_tendencia/', views.canciones_en_tendencia, name='canciones_en_tendencia'),

]   