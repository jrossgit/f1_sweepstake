"""
sweepstake URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import SimpleRouter

from sweepstake import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

router = SimpleRouter()
router.register('teams', views.TeamsViewSet)
router.register('drivers', views.DriversViewSet)
# router.register('seasons', views.SeasonViewSet, base_name='season')
router.register('races', views.RaceResultViewSet)   # todo: look up router naming again
urlpatterns += router.urls
