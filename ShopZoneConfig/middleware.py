import re
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .utils import CustomResponse


class AuthMiddleware(MiddlewareMixin):
    """
    A Middleware to handle JWT authentication for all incoming requests.
    This middleware checks for the presence and validity of the JWT token
    in the Authorization header and sets the request.user attribute.
    """

    def process_request(self, request):
        """
        Process the incoming request to handle JWT authentication.
        """

        # check if the Authorization header is in the correct format
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # authenticate the token and set the user
                user, _ = JWTAuthentication().authenticate(request)
                request.user = user
            except AuthenticationFailed:
                # handle the case where the token is invalid
                return CustomResponse.failed(message="Invalid token", status=403)
        else:
            # handle the case where the token is not provided
            return CustomResponse.failed(message="Authentication credentials were not provided", status=401)

