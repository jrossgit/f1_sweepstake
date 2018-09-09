from random import randint

from django.utils import timezone
from rest_framework import viewsets, generics

from config import TOP_DRIVERS, BOTTOM_DRIVERS
from models import Team, Driver, Race, PlayerSelection
from serializers import TeamSerializer, DriverSerializer, RaceResultSerializer


class TeamsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class DriversViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class RaceResultViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = RaceResultSerializer
    queryset = Race.objects.all()


class GenerateDriversView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        player = Driver.objects.get(pk=request.json['player'])
        race = Race.objects.get(pk=request.json['race'])
        year = timezone.now().year
        qs = Race.objects.filter(date__year=year)
        if not qs.exists():
            qs = Race.objects.filter(date__year=year-1)

        drivers = PlayerSelection.objects.create(
            player=player,
            drivers=self.random_drivers(qs.get_driver_standings()),
            race=race
        )

        return drivers

    @staticmethod
    def random_drivers(drivers):
        count = drivers.count()

        return (
            randint(0, TOP_DRIVERS - 1),
            randint(TOP_DRIVERS, count - BOTTOM_DRIVERS - 1),
            randint(count - BOTTOM_DRIVERS, count - 1)
        )
