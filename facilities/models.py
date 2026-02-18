from django.db import models


class Facility(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        if self.city:
            return f"{self.name} ({self.city})"
        else:
            return self.name
    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
    

class Court(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="courts")
    name = models.CharField(max_length=80)  
    sport = models.CharField(max_length=50, blank=True)  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.facility.name} - {self.name}"