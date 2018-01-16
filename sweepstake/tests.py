# -*- coding: utf-8 -*-

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from rest_framework.test import APITestCase

import models


class DriverTests(DjangoTestCase):

    def setUp(self):
        self.team = models.Team(name='Placeholder', colour='#ff0000')
        self.team.save()

    def test_can_create_drivers(self):

        driver1 = models.Driver()
        driver1.name = 'Joe Bloggs'
        driver1.team = self.team
        driver1.save()
        self.assertEqual(driver1.name, 'Joe Bloggs')
        self.assertEqual(self.team.drivers.count(), 1)

    def test_can_save_unicode_driver(self):

        driver = models.Driver(name=u'Kimi Räikkönen', team=self.team)
        driver.save()
        driver.refresh_from_db()
        self.assertEqual(driver.name, u'Kimi Räikkönen')


class PublicGetTests(APITestCase):

    def setUp(self):
        pass

    def test_get_teams(self):
        """
        Ensure we can create a new account object.
        """
        self.teams_list_url = reverse('team-list')
        response = self.client.get(self.teams_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_get_drivers(self):
        self.driver_list_url = reverse('driver-list')
        response = self.client.get(self.driver_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
