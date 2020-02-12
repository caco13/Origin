from rest_framework import viewsets, status
from rest_framework.response import Response

from risk_profile.risk import Risk
from risk_profile.serializers import UserDataSerializer


class UserDataViewSet(viewsets.ViewSet):
    serializer_class = UserDataSerializer

    @staticmethod
    def create(request):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            risk_profile = Risk(user_data)
            return Response(risk_profile.evaluate(),
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
