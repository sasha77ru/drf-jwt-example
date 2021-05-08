from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    token_stale = models.DateTimeField(null=True)
