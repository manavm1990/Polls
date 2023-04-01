from rest_framework.views import APIView


class UnauthenticatedAPIView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []  # Disable permission checks
