from rest_framework import serializers


class TeamSerializer(serializers.Serializer):

    drivers = serializers.ListField()

    class Meta:
        fields = ('name', 'colour', 'drivers')


class DriverSerializer(serializers.Serializer):

    team = TeamSerializer

    class Meta:
        fields = ('name', 'team')
