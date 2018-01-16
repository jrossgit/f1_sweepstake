import unittest

from selenium import webdriver


class AdminTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_browser_title_is_correct(self):

        self.browser.get('http://localhost:8000')
        self.assertIn('TS Sweepstake', self.browser.title)
