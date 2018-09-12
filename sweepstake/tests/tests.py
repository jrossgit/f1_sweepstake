# -*- coding: utf-8 -*-

from datetime import date

from django.test import TestCase as DjangoTestCase

from sweepstake import models, config
from sweepstake.views import random_3_drivers

class DriverTests(DjangoTestCase):

    def setUp(self):
        self.team = models.Team.objects.create(name='Placeholder', colour='#ff0000')
        self.driver1 = models.Driver.objects.create(name='Joe Bloggs', team=self.team)
        self.driver2 = models.Driver.objects.create(name=u'Kimi Räikkönen', team=self.team)

    def test_can_save_unicode_driver(self):
        self.driver2.refresh_from_db()
        self.assertEqual(self.driver2.name, u'Kimi Räikkönen')


class RaceResultsTest(DjangoTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.teams = [
            models.Team.objects.create(name='Team A', colour='#000000'),
            models.Team.objects.create(name='Team B', colour='#000000'),
            models.Team.objects.create(name='Team C', colour='#000000')
        ]
        cls.drivers = [
            models.Driver.objects.create(name='Driver A1', team=cls.teams[0]),
            models.Driver.objects.create(name='Driver B1', team=cls.teams[1]),
            models.Driver.objects.create(name='Driver C1', team=cls.teams[2]),
            models.Driver.objects.create(name='Driver A2', team=cls.teams[0]),
            models.Driver.objects.create(name='Driver B2', team=cls.teams[1]),
            models.Driver.objects.create(name='Driver C2', team=cls.teams[2]),
            models.Driver.objects.create(name='Driver Extra', team=cls.teams[2], active=False)
        ]

        cls.race = models.Race.objects.create(name='Moldovan GP', date=date(2017, 1, 1))
        cls.unraced_race = models.Race.objects.create(name='Kyrgyzstani GP', date=date(2017, 1, 2))
        cls.race.set_fastest_lap(cls.drivers[1])
        cls.race.set_pole(cls.drivers[2])
        cls.race.set_results(cls.drivers[:6], 6)
        cls.race.save()
        cls.race.activate()

    def test_unicode_string_for_race(self):
        self.assertEqual(u'2017 Moldovan GP', str(self.race))

    def test_race_in_correct_season(self):
        self.assertEqual(self.race.season, u'2017')

    def test_winning_driver_scores_top_points(self):
        self.assertEqual(self.race.points_for_driver(self.drivers[0]), 6)
        self.assertEqual(self.race.points_for_driver(self.drivers[3]), 3)

    def test_pole_driver_scores_points(self):
        self.assertEqual(self.race.points_for_driver(self.drivers[2]), 4 + config.POINTS_FOR_POLE)

    def test_fastest_lap_driver_scores_points(self):
        self.assertEqual(self.race.points_for_driver(self.drivers[1]), 5 + config.POINTS_FOR_FASTEST_LAP)

    def test_race_table_for_one_race(self):
        race_table = models.Race.objects.filter(name='Moldovan GP').get_driver_standings()
        self.assertEqual(race_table[5], self.drivers[5])
        self.assertEqual(race_table[0].total_points, 5 + config.POINTS_FOR_FASTEST_LAP)
        self.assertEqual(len(race_table), 6)


class TestSelectionGeneration(DjangoTestCase):

    @classmethod
    def setUpTestData(cls):
        team = models.Team.objects.create(name='Team C', colour='#000000')
        cls.drivers = [
            models.Driver.objects.create(name='Driver A1', team=team),
            models.Driver.objects.create(name='Driver B1', team=team),
            models.Driver.objects.create(name='Driver C1', team=team),
        ]
        player = models.Player.objects.create(name='Joe')
        cls.race = models.Race.objects.create(name='Turkmenistani GP', date=date(2018, 1, 1))
        cls.selection = models.PlayerSelection.objects.create(player=player, race=cls.race)
        cls.selection.drivers.set(cls.drivers)

    def test_that_it_generates_three_distinct_drivers(self):
        self.assertEqual(self.drivers, random_3_drivers(models.Driver.objects.all(), 1, 1))

    def test_that_it_evaluates_points(self):
        self.assertEqual(None, self.selection.points)
        self.race.set_results(self.drivers, 3)
        self.selection.set_points()
        self.assertEqual(6, self.selection.points)
