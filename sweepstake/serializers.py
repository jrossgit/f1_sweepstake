from rest_framework import serializers
from sweepstake import models


class SimpleTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Team
        fields = ('name', 'colour')


class DriverSerializer(serializers.ModelSerializer):

    team = SimpleTeamSerializer()

    class Meta:
        model = models.Driver
        fields = ('name', 'team')


class TeamSerializer(serializers.ModelSerializer):

    drivers = DriverSerializer

    class Meta:
        model = models.Team
        fields = ('name', 'colour', 'drivers')


class RaceResultSerializer(serializers.ModelSerializer):

    fastest_lap = serializers.SerializerMethodField()

    pole = serializers.SerializerMethodField()

    class Meta:
        model = models.Race
        fields = ('name', 'date', 'fastest_lap', 'pole', 'results')

    def get_fastest_lap(self, instance, *args, **kwargs):
        return DriverSerializer(models.PointsValue.objects.get(race=instance, fastest_lap=True).driver).data

    def get_pole(self, instance, *args, **kwargs):
        return DriverSerializer(models.PointsValue.objects.get(race=instance, pole=True).driver).data


class RaceResultSummarySerializer(serializers.ModelSerializer):

    winner = serializers.SerializerMethodField()
    class Meta:
        model = models.Race
        fields = ('id', 'name', 'date', 'winner')

    def get_winner(self, instance, *args, **kwargs):
        return DriverSerializer(models.PointsValue.objects.get(race=instance, position=1).driver).data
