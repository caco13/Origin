from rest_framework import serializers

from risk_profile.objects import UserData


class HouseSerializer(serializers.Serializer):
    STATUSES = ('owned', 'mortgaged')

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
    house = HouseSerializer()
    income = serializers.IntegerField()
    marital_status = serializers.ChoiceField(choices=STATUSES)
    risk_questions = serializers.ListField(child=serializers.BooleanField())
    vehicle = VehicleSerializer()

    def create(self, validated_data):
        return UserData(**validated_data)

    def update(self, instance, validated_data):
        pass
