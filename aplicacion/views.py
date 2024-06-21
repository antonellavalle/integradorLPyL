from django.shortcuts import get_object_or_404, render, redirect
import requests
from .models import Usuario

"""
La función listar_usuarios muestra una lista de todos los usuarios registrados.
"""
def listar_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})  # Renderiza la plantilla listar_usuarios.html con la lista de usuarios

"""
La función detalle_usuario muestra los detalles de un usuario específico.
"""
def detalle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)  # Obtiene el usuario específico o retorna un 404 si no existe
    return render(request, 'detalle_usuario.html', {'usuario': usuario})  # Renderiza la plantilla detalle_usuario.html con los detalles del usuario

"""
La función editar_usuario maneja la edición de los datos de un usuario específico.
"""
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)  # Obtiene el usuario específico o retorna un 404 si no existe
    
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        # Aquí iría la lógica para editar el usuario
        return redirect('detalle_usuario', pk=pk)  # Redirige a la vista de detalles del usuario después de editarlo
    else:
        return render(request, 'editar_usuario.html', {'usuario': usuario})  # Renderiza la plantilla editar_usuario.html con los datos del usuario

"""
La función eliminar_usuario maneja la eliminación de un usuario específico.
"""
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)  # Obtiene el usuario específico o retorna un 404 si no existe
    
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        # Aquí iría la lógica para eliminar el usuario
        return redirect('listar_usuarios')  # Redirige a la vista de lista de usuarios después de eliminarlo
    else:
        return render(request, 'eliminar_usuario.html', {'usuario': usuario})  # Renderiza la plantilla eliminar_usuario.html con los datos del usuario
