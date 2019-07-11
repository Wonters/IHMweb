# Create your models here.

from django.db import models


class ProgressCalib(models.Model):
    current = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    message = models.CharField(max_length=200)