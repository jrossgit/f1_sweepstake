from rest_framework import serializers
import models

class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Driver
        fields = ('name', 'team')


class TeamSerializer(serializers.ModelSerializer):

    drivers = DriverSerializer

    class Meta:
        model = models.Team
        fields = ('name', 'colour', 'drivers')


class RaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Race
        fields = ('name', 'date', 'fastest_lap', 'pole', 'results')


class SeasonSerializer(serializers.ModelSerializer):
    pass # only allow detail views
