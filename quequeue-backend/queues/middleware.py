from django.conf import settings
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class SessionDebugMiddleware:
    """Development middleware to debug session issues"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only run in debug mode
        if not settings.DEBUG:
            return self.get_response(request)
        
        # Log session info for API requests
        if request.path.startswith('/api/'):
            session_key = request.session.session_key
            has_user_id = 'user_id' in request.session
            logger.info(f"API Request: {request.path}, Session Key: {session_key}, Has user_id: {has_user_id}")
            
            # If session exists but user_id is in session, check if user exists
            if has_user_id:
                from .models import User
                user_id = request.session.get('user_id')
                try:
                    User.objects.get(pk=user_id)
                    logger.info(f"User {user_id} exists in database")
                except User.DoesNotExist:
                    logger.warning(f"User {user_id} in session but not in database - clearing session")
                    request.session.flush()

        response = self.get_response(request)
        return response