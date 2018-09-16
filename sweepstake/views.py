from random import randint

from django.utils import timezone
from rest_framework import viewsets, generics

from sweepstake.config import TOP_DRIVERS, BOTTOM_DRIVERS
from sweepstake.models import Team, Driver, Race, PlayerSelection
from sweepstake.serializers import TeamSerializer, DriverSerializer, RaceResultSerializer, RaceResultSummarySerializer


class TeamsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class DriversViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class RaceResultViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = RaceResultSerializer
    queryset = Race.objects.all()


class SimpleRaceResultView(generics.ListAPIView):
    # queryset = Race.objects.all()
    serializer_class = RaceResultSummarySerializer
    lookup_field = 'date__year'
    lookup_url_kwarg = 'season'

    def get_queryset(self, *args, **kwargs):
        return Race.objects.filter(date__year=kwargs['date__year'])


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
            drivers=random_3_drivers(qs.get_driver_standings()),
            race=race
        )

        return drivers


def random_3_drivers(drivers, top_drivers=TOP_DRIVERS, bottom_drivers=BOTTOM_DRIVERS):
    count = drivers.count()
    indices = (
        randint(0, top_drivers - 1),
        randint(top_drivers, count - bottom_drivers - 1),
        randint(count - bottom_drivers, count - 1)
    )
    return [drivers[i] for i in indices]
