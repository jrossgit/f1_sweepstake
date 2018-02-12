from rest_framework import viewsets, generics

from models import Team, Driver, Race
from serializers import TeamSerializer, DriverSerializer, SeasonSerializer, RaceSerializer


class TeamsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class DriversViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


# class SeasonView(generics.ListAPIView):
#
#     serializer_class = SeasonSerializer
#
#     def get_queryset(self):
#


class RaceResultViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = RaceSerializer
    queryset = Race.objects.all()
