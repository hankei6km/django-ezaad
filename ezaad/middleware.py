from django.http.response import HttpResponse
from django.urls import reverse

from django_scim.settings import scim_settings
from django_scim.middleware import SCIMAuthCheckMiddleware


class SCIMAuthCheckMiddleware(SCIMAuthCheckMiddleware):
    def process_request(self, request):
        if self.should_log_request(request):
            self.log_request(request)
        # If we've just passed through the auth middleware and there is no user
        # associated with the request we can assume permission
        # was denied and return a 401.
        if not hasattr(request, 'user') or request.user.is_anonymous or not request.user.is_superuser:
            if request.path.startswith(self.reverse_url):
                response = HttpResponse(status=401)
                response['WWW-Authenticate'] = scim_settings.WWW_AUTHENTICATE_HEADER
                return response