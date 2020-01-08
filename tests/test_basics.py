import unittest

from flask import current_app
from apps import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app_exists(self):
        pass

    def test_app_is_testing(self):
        pass
