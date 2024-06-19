import logging
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)  # Define el logger para este módulo usando __name__

class AutenticacionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f'Middleware llamado para la URL: {request.path}')

        if request.user.is_authenticated or request.path.startswith('/login/'):
            response = self.get_response(request)
        else:
            logger.debug('Usuario no autenticado. Redirigiendo a iniciar_sesion.')
            return redirect(reverse('iniciar_sesion'))
        
        return response
