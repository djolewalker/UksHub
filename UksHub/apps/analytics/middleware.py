from UksHub.apps.analytics.models import Visit
from django.utils import timezone

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.is_ajax() is not True:
            if request.session.session_key is None and request.session.exists(request.session.session_key) is False:
                request.session.save()
            visit = Visit()
            visit.path = request.path
            visit.session_id  = request.session.session_key
            visit.host = self.get_client_ip(request)
            visit.time = timezone.now()
            if request.user.is_authenticated:
                visit.user = request.user
        response = self.get_response(request)
        visit.responseCode = response.status_code
        visit.save()
        return response




    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')