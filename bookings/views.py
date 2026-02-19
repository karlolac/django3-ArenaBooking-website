from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.contrib import messages

from facilities.models import Court
from .models import Booking
from .forms import BookingForm

def bookings(request):
    now = timezone.now()

    user_bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("court")
        .order_by("-start_datetime")
    )

    active_bookings = user_bookings.filter(end_datetime__gt=now)
    past_bookings = user_bookings.filter(end_datetime__lte=now)

    return render(request, "bookings/bookings.html", {
        "active_bookings": active_bookings,
        "past_bookings": past_bookings,
        "now": now,
    })


@login_required
def bookcourt(request, court_id):
    court = get_object_or_404(Court, id=court_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.court = court
            booking.save()
            return redirect("bookings:bookings")
    else:
        form = BookingForm()

    return render(request, "bookings/bookcourt.html", {
        "court": court,
        "form": form
    })
