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

    def setUpClass(cls):
        cls.team = models.Team.objects.create(name='Placeholder', colour='#ff0000')
        cls.driver1 = models.Driver.objects.create(name='Joe Bloggs', team=cls.team)
        cls.driver2 = models.Driver.objects.create(name=u'Kimi Räikkönen', team=cls.team)
        cls.race = models.Race.objects.create(name='Nicaraguan GP', date=date(2017,1,5))
        cls.race = models.Race.objects.create(name='Burmese GP', date=date(2018,1,5))

