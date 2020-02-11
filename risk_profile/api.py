from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

from risk_profile.objects import UserData


# Serializer
class UserDataSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return UserData(**validated_data)

    def update(self, instance, validated_data):
        pass


# View
class UserDataViewSet(viewsets.ViewSet):
    serializer_class = UserDataSerializer

    def create(self, request):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
