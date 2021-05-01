from django.db import models
from rest_framework.authtoken.models import Token


class ExpiringToken(Token):
    last_action = models.DateTimeField(auto_now=True)