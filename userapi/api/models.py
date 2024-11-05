from django.db import models

class  User(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=20, unique=True)
    profession = models.CharField(max_length=20)
    age = models.IntegerField()
