from django.db import models

# Create your models here.


class day_data(models.Model):
    name = models.CharField(max_length=20)
