from django.test import TestCase
from .modules.validInputs import *

class validationTests(TestCase):
    def setUp(self):
        self.mail = 'loicmartins.com@gmail'
        self.name = 'Henok05'
        self.profession = 'Actor02'
        self.age = 61
    
    def test_mail_validation(self):
        self.assertEqual(validMail(self.mail), False)
    
    def test_username_validation(self):
        self.assertEqual(validname(self.name), False)

    def test_profession_validation(self):
        self.assertEqual(validProfession(self.profession), False)

    def test_age_validation(self):
        self.assertEqual(validAge(self.age), False)