# from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from djongo import models

class UserModel(models.Model):
    username=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    first_name=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)

    def __str__(self):
        return self.username