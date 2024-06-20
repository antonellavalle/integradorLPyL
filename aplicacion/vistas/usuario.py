# views/usuario.py

from django.shortcuts import get_object_or_404, render, redirect
from aplicacion.models import Usuario
from django.views import View

class UsuarioListView(View):
    """Vista para listar todos los usuarios."""
    def get(self, request):
        usuarios = Usuario.objects.all()
        return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

class UsuarioDetailView(View):
    """Vista para mostrar los detalles de un usuario específico."""
    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        return render(request, 'detalle_usuario.html', {'usuario': usuario})

class UsuarioEditView(View):
    """Vista para editar los datos de un usuario específico."""
    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        return render(request, 'editar_usuario.html', {'usuario': usuario})

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        # Capturamos los datos del formulario.
        nuevo_nombre = request.POST.get('nombre')
        nuevo_correo = request.POST.get('correo')

        # Verificamos y actualizamos los campos.
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
        if nuevo_correo:
            usuario.correo = nuevo_correo

        usuario.save()  # Guardamos los cambios.
        return redirect('detalle_usuario', pk=pk)

class UsuarioDeleteView(View):
    """Vista para eliminar un usuario específico."""
    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        return render(request, 'eliminar_usuario.html', {'usuario': usuario})

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        usuario.delete()
        return redirect('listar_usuarios')
