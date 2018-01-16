"""
sweepstake URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import SimpleRouter

import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

router = SimpleRouter()
router.register('teams', views.TeamsViewSet)
router.register('drivers', views.DriversViewSet)
urlpatterns += router.urls