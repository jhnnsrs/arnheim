from django.test import RequestFactory
from rest_framework.settings import api_settings
from larvik.logging import get_module_logger

logger = get_module_logger(__name__)

class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        # Look up user from query string (you should also do things like
        # check it's a valid user ID, or if scope["user"] is already populated)
        line = str(scope["query_string"])

        if "user" in scope:
            if scope["user"] is not None:
                return self.inner(dict(scope))
            else:
                pass

        auth_token = None
        try:
            auth_token = line.split('token=')[-1][0:-1]
        except AttributeError:
            logger.error("No token provided")
            pass

        user = None

        if auth_token:
            # compatibility with rest framework

            rf = RequestFactory()
            get_request = rf.get('/api/comments/')
            get_request._request = {}
            get_request.method = "GET"
            get_request.META["HTTP_AUTHORIZATION"] = "Bearer {}".format(auth_token)

            authenticators = [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]
            for authenticator in authenticators:
                user_auth_tuple = None
                user_auth_tuple = authenticator.authenticate(get_request)
                if user_auth_tuple is not None:
                    user, auth = user_auth_tuple
                    break

        # Return the inner application directly and let it run everything else
        return self.inner(dict(scope, user=user))