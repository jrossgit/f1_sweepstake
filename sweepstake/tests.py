# -*- coding: utf-8 -*-

from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APITransactionTestCase

import models, config


class DriverTests(DjangoTestCase):

    def setUp(self):
        self.team = models.Team.objects.create(name='Placeholder', colour='#ff0000')
        self.driver1 = models.Driver.objects.create(name='Joe Bloggs', team=self.team)
        self.driver2 = models.Driver.objects.create(name=u'Kimi Räikkönen', team=self.team)

    def test_can_create_drivers(self):
        self.assertEqual(self.driver1.name, 'Joe Bloggs')
        self.assertEqual(self.team.drivers.count(), 2)

    def test_can_save_unicode_driver(self):
        self.driver2.refresh_from_db()
        self.assertEqual(self.driver2.name, u'Kimi Räikkönen')
        self.assertIn(u'Kimi Räikkönen', unicode(self.driver2))


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
        self.assertEqual(u'2017 Moldovan GP', unicode(self.race))

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


class PreviousYearTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.team = models.Team.objects.create(name='Placeholder', colour='#ff0000')
        cls.driver1 = models.Driver.objects.create(name='Joe Bloggs', team=cls.team)
        cls.driver2 = models.Driver.objects.create(name=u'Kimi Räikkönen', team=cls.team)
        cls.race = models.Race.objects.create(name='Yemeni GP', date=date(2017,1,5))

        cls.race.activate()
        cls.race.set_results([cls.driver1, cls.driver2], 2)
        cls.race.set_pole(cls.driver1)
        cls.race.set_fastest_lap(cls.driver2)

    def test_get_teams(self):
        """
        Ensure we can create a new account object.
        """
        teams_list_url = reverse('team-list')
        response = self.client.get(teams_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_get_drivers(self):
        driver_list_url = reverse('driver-list')
        response = self.client.get(driver_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_get_race_result(self):
        race_result_url = reverse('race-detail', kwargs={'pk': self.race.pk})
        response = self.client.get(race_result_url)
        print response
        self.assertEqual(response.status_code, 200)

    def test_get_missing_race_result(self):
        race_result_url = reverse('race-detail', kwargs={'pk': 10})
        response = self.client.get(race_result_url)
        self.assertEqual(response.status_code, 404)

    # def test_get_season_result(self):
    #     season_result_url = reverse('season-detail', kwargs={'year': 2017})
    #     response = self.client.get(season_result_url)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_get_missing_season_result(self):
    #     season_result_url = reverse('season-detail', kwargs={'year': 2020})
    #     response = self.client.get(season_result_url)
    #     self.assertEqual(response.status_code, 404)


# class DriverSelectionTest(DjangoTestCase):
#
#     def setUp(self):
