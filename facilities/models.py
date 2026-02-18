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
    class Sport(models.TextChoices):
        FOOTBALL = "football", "Nogomet"
        BASKETBALL = "basketball", "Košarka"
        TENNIS = "tennis", "Tenis"
        PADEL = "padel", "Padel"
        OTHER = "other", "Ostalo"
   
    sport = models.CharField(
    max_length=20,
    choices=Sport.choices,
    blank=True,
    null=True
    )
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="courts")
    name = models.CharField(max_length=80)  
    is_active = models.BooleanField(default=True)


    def __str__(self):
        if self.sport:
            return f"{self.facility.name} - {self.name} ({self.get_sport_display()})"
        return f"{self.facility.name} - {self.name}"