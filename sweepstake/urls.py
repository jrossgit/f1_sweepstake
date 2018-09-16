"""
sweepstake URL Configuration
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import SimpleRouter

from sweepstake import views

season_urls = [

]

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path('season/<int:year>/', include(season_urls)),
]

router = SimpleRouter()
router.register('teams', views.TeamsViewSet)
router.register('drivers', views.DriversViewSet)
router.register('races', views.RaceResultViewSet)   # todo: look up router naming again
urlpatterns += router.urls
