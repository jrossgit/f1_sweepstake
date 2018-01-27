# -*- coding: utf-8 -*-
from datetime import datetime, date

from django.db import models
from django.contrib import admin

import config

class Player(models.Model):

    name = models.CharField(max_length=30)


class Race(models.Model):

    name = models.CharField(max_length=30)
    date = models.DateField(unique=True)
    fastest_lap = models.ForeignKey('Driver', related_name='fastest_laps', null=True, blank=True)
    pole = models.ForeignKey('Driver', related_name='poles', null=True, blank=True)

    class Meta:
        order_with_respect_to = 'date'

    def __unicode__(self):
        return '{} {}'.format(self.season, self.name)

    @property
    def season(self):
        return unicode(self.date.year)

    def activate(self):
        for driver in Driver.objects.filter(active=True):
            DriverResult.objects.create(race=self, driver=driver)

    def points_for_driver(self, driver):
        result = DriverResult.objects.get(race=self, driver=driver)
        if result.classified is None:
            raise RuntimeError('Race must be completed before evaluating points')

        points = self.results.count() - result.position
        points += config.POINTS_FOR_FASTEST_LAP if self.fastest_lap == driver else 0
        points += config.POINTS_FOR_POLE if self.pole == driver else 0
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

    race = models.ForeignKey(Race, related_name='results')
    driver = models.ForeignKey(Driver, related_name='results')
    position = models.IntegerField(null=True, blank=True)
    classified = models.NullBooleanField()

    def __unicode__(self):
        return u'<Result: {}, {}>'.format(self.race, self.driver)

    class Meta:
        unique_together = (('race', 'position'),)



admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(Race)
admin.site.register(Player)
