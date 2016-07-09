from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserDB(models.Model):
    order = models.CharField(max_length=100)
    person = models.CharField(max_length=100)
    email = models.EmailField()
    pay_value = models.FloatField(null=True)
    pay_method=models.CharField(null=True, max_length=10)
    comment = models.CharField(null=True, max_length=300)