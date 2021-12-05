from django.db import models

# Create your models here.

class Log(models.Model):
    select = models.CharField(max_length=100, null=True)
    info = models.TextField(null=True)
    sim = models.IntegerField(null=True)
    result = models.TextField(null=True)
