from django.db import models


class Bus(models.Model):
    name     = models.CharField(max_length=50)
    route    = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BusLocation(models.Model):
    bus       = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='locations')
    latitude  = models.FloatField()
    longitude = models.FloatField()
    speed     = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.name} @ {self.timestamp}"
