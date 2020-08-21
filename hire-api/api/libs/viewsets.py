# django and rest_framework imports
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


class ModelViewSetWithoutDelete(viewsets.ModelViewSet):
    """
    """
    def destroy(self, request, *args, **kwargs):
        """
        overrides the destroy method
        """
        return Response(status=status.HTTP_204_NO_CONTENT)
