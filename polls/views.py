from rest_framework.generics import RetrieveAPIView


class UnauthenticatedRetrieveAPIView(RetrieveAPIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks
