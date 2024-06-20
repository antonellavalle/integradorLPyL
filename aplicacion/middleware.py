import logging
from django.shortcuts import redirect
from django.urls import reverse
import re

logger = logging.getLogger(__name__)

class AutenticacionMiddleware:
    def __init__(self, get_response):  # Corrige el método __init__
        self.get_response = get_response
        # Añade los patrones de URL que quieres excluir de la autenticación
        self.excluded_urls = [
            re.compile(r'^/signup/$'),  # URL exacta para registro
            re.compile(r'^/login/$'),   # URL exacta para inicio de sesión
            re.compile(r'^/$'),         # URL para la página de inicio, si es necesario
        ]

    def __call__(self, request):  # Corrige el método __call__
        logger.debug(f'Middleware llamado para la URL: {request.path}')
        print(f'URL solicitada: {request.path}')  # Añadir esta línea para depurar

        # Verifica si la URL debe ser excluida
        if any(pattern.match(request.path) for pattern in self.excluded_urls):
            logger.debug(f'URL {request.path} excluida del middleware.')
            return self.get_response(request)

        # Verifica si el usuario está autenticado
        if request.user.is_authenticated or request.path == reverse('signup'):
            logger.debug('Usuario autenticado o página de registro. Continuando con la solicitud.')
            return self.get_response(request)
        else:
            logger.debug('Usuario no autenticado. Redirigiendo a iniciar_sesion.')
            return redirect(reverse('iniciar_sesion'))
