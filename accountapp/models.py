from django.db import models

# Create your models here.

class main_slogan(models.Model):
    content = models.CharField(max_length=255, null=False)
    date = models.DateField(auto_now=True) 