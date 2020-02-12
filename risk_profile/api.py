from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

from risk_profile.objects import UserData


# Serializers
class HouseSerializer(serializers.Serializer):
    STATUSES = ('owner', 'mortgaged')

    ownership_status = serializers.ChoiceField(
        choices=STATUSES, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class VehicleSerializer(serializers.Serializer):
    year = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserDataSerializer(serializers.Serializer):
    STATUSES = ('single', 'married')

    age = serializers.IntegerField()
    dependents = serializers.IntegerField()
    house = HouseSerializer(required=False)
    income = serializers.IntegerField()
    marital_status = serializers.ChoiceField(choices=STATUSES)
    risk_questions = serializers.ListField(child=serializers.BooleanField())
    vehicle = VehicleSerializer(required=False)

    def create(self, validated_data):
        return UserData(**validated_data)

    def update(self, instance, validated_data):
        pass


# Views
class UserDataViewSet(viewsets.ViewSet):
    serializer_class = UserDataSerializer

    def create(self, request):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
