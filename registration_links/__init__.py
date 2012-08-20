from django.conf import settings
from registration.backends.simple import SimpleBackend


class SimpleBackend(SimpleBackend):
    """
    Slightly modified django_registration SimpleBackend
    """

    def registration_allowed(self, request):
        """
        Overloading method that checks if the registration is allowed.
        When you use this module, user must use the valid link (that sets the session variable)
        to access the registration view.
        """
        return request.session.get("reg_link", False) != False and getattr(settings, 'REGISTRATION_OPEN', True)
