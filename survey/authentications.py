from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return