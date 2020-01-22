from django.db import models

# Create your models here.


class day_record(models.Model):
    sortid = models.IntegerField(default=0)
    province = models.CharField(default=None, max_length=50)
    city = models.CharField(default=None, max_length=50)
    AQI = models.IntegerField(default=0)
    air_quality = models.CharField(default=None, max_length=50)
    PM = models.IntegerField(default=0)
    key_pollution = models.CharField(default=None, max_length=50)
    release_time = models.DateField()
    last_update_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.release_time)+self.city+str(self.AQI)
