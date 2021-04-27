from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class MyUser(AbstractUser):
    wallet = models.IntegerField(default=10000, validators=[MinValueValidator(0)])
