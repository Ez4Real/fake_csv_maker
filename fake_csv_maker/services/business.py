from django.contrib.auth.models import User
from django.http import HttpRequest

def get_current_user(request: HttpRequest) -> User:
    '''
    Returns current user from request
    '''
    return request.user