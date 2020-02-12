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


def greater_than_zero(value):
    if value < 0:
        raise serializers.ValidationError('Must be greater than 0')


class UserDataSerializer(serializers.Serializer):
    STATUSES = ('single', 'married')

    age = serializers.IntegerField(validators=[greater_than_zero])
    dependents = serializers.IntegerField(validators=[greater_than_zero])
    house = HouseSerializer()
    income = serializers.IntegerField(validators=[greater_than_zero])
    marital_status = serializers.ChoiceField(choices=STATUSES)
    risk_questions = serializers.ListField(child=serializers.BooleanField())
    vehicle = VehicleSerializer()

    def create(self, validated_data):
        return UserData(**validated_data)

    def update(self, instance, validated_data):
        pass


