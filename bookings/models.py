from django.db import models
from django.contrib.auth.models import User
from facilities.models import Court


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="bookings")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

   
    STATUS_CHOICES = [
        ('pending', 'Na čekanju'),
        ('confirmed', 'Potvrđeno'),
        ('cancelled', 'Otkazano'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    def __str__(self):
        return f"{self.user.username} | {self.court} | {self.start_datetime.strftime('%d.%m. %H:%M')} ({self.get_status_display()})"
    
    class Meta:
        permissions = [
        ("can_approve_booking", "Can approve booking"),
    ]