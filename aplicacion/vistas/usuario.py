from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from aplicacion.forms import UserUpdateForm

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'editar_usuario.html'
    success_message = "Perfil actualizado con éxito"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance = self.get_object()
        form.request = self.request  # Pasar la solicitud al formulario
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return reverse('editar_usuario')

