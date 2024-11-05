from django.test import TestCase
from models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create()