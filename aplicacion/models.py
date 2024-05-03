from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    seguidos = models.ManyToManyField('self', symmetrical=False, related_name='seguidores')
    '''grupos = models.ManyToManyField('Grupo', related_name='miembros')'''

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)

class Album(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    ano_lanzamiento = models.IntegerField()
    '''discografica = models.ForeignKey(Discografica, on_delete=models.SET_NULL, null=True, blank=True)'''

class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    duracion = models.DurationField()

class ListaReproduccion(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    canciones = models.ManyToManyField(Cancion)

class Discografica(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

class ValoracionCancion(models.Model):
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valoracion = models.IntegerField()  # Puntuación de la canción (ej: 1 al 5)

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    '''miembros = models.ManyToManyField(User, related_name='grupos')'''
    canciones = models.ManyToManyField('Cancion', related_name='grupos')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre