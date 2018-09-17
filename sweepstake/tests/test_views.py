"""
    test_views

    Copyright TotalSim Ltd, 2018 all rights reserved
        jross (james@totalsim.co.uk)

    The contents of this file are NOT for redistribution
    Please see the README.md file distributed with this source code
"""
from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase

from sweepstake import models


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

    def test_can_get_teams(self):
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
        self.assertEqual(response.status_code, 200)

    def test_get_missing_race_result(self):
        race_result_url = reverse('race-detail', kwargs={'pk': 10})
        response = self.client.get(race_result_url)
        self.assertEqual(response.status_code, 404)



class SeasonSpecificViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.team = models.Team.objects.create(name='Placeholder', colour='#ff0000')
        cls.driver1 = models.Driver.objects.create(pk=1, name='Joe Bloggs', team=cls.team)
        cls.driver2 = models.Driver.objects.create(pk=2, name=u'Kimi Räikkönen', team=cls.team)
        cls.race_last_year = models.Race.objects.create(name='Nicaraguan GP', date=date(2017,1,5))
        cls.race_this_year = models.Race.objects.create(name='Burmese GP', date=date(2018,1,5))
        cls.race_this_year.set_results([cls.driver1, cls.driver2], 2)
        cls.race_last_year.set_results([cls.driver2, cls.driver1], 2)

    def test_that_correct_race_is_selected(self):
        season_url = reverse('season-detail', kwargs={'season': 2018})
        response = self.client.get(season_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.race_this_year.name)
        self.assertEqual(response.data[0]['winner']['name'], self.driver1.name)

    def test_that_correct_race_results_are_selected(self):
        race_url = reverse('season-detail', kwargs={'season': 2018, 'race': 1})
        response = self.client.get(race_url)
        self.assertEqual(response.data['name'], self.race_this_year.name)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['driver']['name'], self.driver1.name)