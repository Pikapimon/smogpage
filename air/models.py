from django.db import models

# Create your models here.


class day_record(models.Model):
    time = models.DateField()
    city_id = models.IntegerField(default=0)
    province = models.CharField(default=None, max_length=50)
    city = models.CharField(default=None, max_length=50)
    AQI = models.IntegerField(default=0)
    air_quality = models.CharField(default=None, max_length=50)
    PM2_5 = models.IntegerField(default=0)
    pm10 = models.IntegerField(default=0)
    co = models.IntegerField(default=0)
    no2 = models.IntegerField(default=0)
    o3 = models.IntegerField(default=0)
    so2 = models.IntegerField(default=0)

    def __str__(self):
        return str(self.release_time)+self.city+str(self.AQI)
