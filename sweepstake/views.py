from rest_framework import viewsets

from models import Team, Driver
from serializers import TeamSerializer, DriverSerializer


class TeamsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class DriversViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = DriverSerializer
    queryset = Driver.objects.all()