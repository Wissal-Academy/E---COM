from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import APIToken


class CustomTokenAuthentification(BaseAuthentication):
    def authenticate(self, request):
        # GET THE AUTHORIZATION TOKEN FROM THE REQUEST
        auth_header = request.headers.get('Authorization')
        # CHECK IF THE AUTHORIZATION HEADER EXITS
        # IF IT EXISTS CHECK IF STARTS WITH "TOKEN "
        if not auth_header or not auth_header.startswith('Token '):
            return None

        # Authorization : >>> "Token e9d047bd-2ccb-4b87-81e0-624ac4c8f8f3"
        # ['Token' ,'e9d047bd-2ccb-4b87-81e0-624ac4c8f8f3']
        token_key = auth_header.split(' ')[1]
        try:
            token = APIToken.objects.get(token=token_key)
        except APIToken.DoesNotExist:
            raise AuthenticationFailed('Invalid Token')
        return (token.user, None)
