# -*- coding: utf-8 -*-
from datetime import datetime, date

from django.db import models
from django.db.models import Sum
from django.contrib import admin

import config

class Player(models.Model):

    name = models.CharField(max_length=30)


class RaceQuerySet(models.QuerySet):

    def get_driver_standings(self):
        points = PointsValue.objects.filter(race__in=self, points__isnull=False)

        table = Driver.objects.filter(points__in=points).annotate(
            total_points=Sum('points__points')
        ).order_by('-total_points')

        return table


class Race(models.Model):

    objects = RaceQuerySet.as_manager()

    name = models.CharField(max_length=30)
    date = models.DateField(unique=True)
    results = models.ManyToManyField('PointsValue', related_query_name='race', blank=True)

    class Meta:
        order_with_respect_to = 'date'

    def __unicode__(self):
        return '{} {}'.format(self.season, self.name)

    @property
    def season(self):
        return unicode(self.date.year)

    def set_fastest_lap(self, driver):
        self.results.add(
            PointsValue.objects.create(
                driver=driver,
                points=config.POINTS_FOR_FASTEST_LAP,
                fastest_lap=True
            )
        )

    def set_pole(self, driver):
        self.results.add(
            PointsValue.objects.create(driver=driver, points=config.POINTS_FOR_POLE, pole=True)
        )

    def set_results(self, driver_list, finishers):

        for index, driver in enumerate(driver_list):
            finished = index + 1 < finishers
            self.results.add(PointsValue.objects.create(
                driver=driver,
                position=index+1,
                points=len(driver_list)-index,
                classified=finished
                ))

        self.save()

    def get_results(self):
        return Driver.objects.filter(points__isnull=False).annotate(
            total_points=Sum('points__points')
        ).order_by('-total_points')

    def activate(self):
        for driver in Driver.objects.filter(active=True):
            DriverResult.objects.create(race=self, driver=driver)

    def points_for_driver(self, driver):

        points = PointsValue.objects.filter(
            driver=driver,
            race=self
        ).aggregate(models.Sum('points'))['points__sum']
        return points


class Team(models.Model):

    name = models.CharField(max_length=30)
    colour = models.CharField(max_length=7)  # Hex code string, e.g. '#ff0000'
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'<Team: {}>'.format(self.name)


class Driver(models.Model):

    active = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    team = models.ForeignKey(Team, related_name='drivers')

    def __unicode__(self):
        return u'<Driver: {}>'.format(self.name)


class DriverResult(models.Model):

    race = models.ForeignKey(Race, related_name='race_results')
    driver = models.ForeignKey(Driver, related_name='race_results')
    position = models.IntegerField(null=True, blank=True)
    classified = models.NullBooleanField()

    def __unicode__(self):
        return u'<Result: {}, {}>'.format(self.race, self.driver)

    class Meta:
        unique_together = (('race', 'position'),)


class PointsValue(models.Model):
    """race is available as a foreignkey"""
    driver = models.ForeignKey(Driver, related_name='points')
    points = models.IntegerField()
    position = models.IntegerField(null=True, blank=True)
    fastest_lap = models.BooleanField(default=False)
    pole = models.BooleanField(default=False)
    classified = models.NullBooleanField()


class PlayerSelection(models.Model):
    race = models.ForeignKey(Race, related_name='selections')
    player = models.ForeignKey(Player, related_name='selections')
    drivers = models.ManyToManyField(Driver, max_length=3)


admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(Race)
admin.site.register(Player)
admin.site.register(PlayerSelection)
admin.site.register(PointsValue)
