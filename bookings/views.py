from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from facilities.models import Court
from .models import Booking
from .forms import BookingForm

@login_required
def bookings(request):
    now = timezone.now()

    user_bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("court")
        .order_by("-start_datetime")
    )

    active_bookings = user_bookings.filter(end_datetime__gt=now).order_by("start_datetime")
    past_bookings = user_bookings.filter(end_datetime__lte=now).order_by("-start_datetime")

    return render(request, "bookings/bookings.html", {
        "active_bookings": active_bookings,
        "past_bookings": past_bookings,
        "now": now,
    })


@login_required
def bookcourt(request, court_id):
    court = get_object_or_404(Court, id=court_id)

    if request.method == "POST":
        form = BookingForm(request.POST, court_id=court_id)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.court = court
            booking.save()
            
            messages.success(request, "Vaša rezervacija je uspješno potvrđena!")
            
            return redirect("bookings:bookings")
    else:
        form = BookingForm(court_id=court_id)

    return render(request, "bookings/bookcourt.html", {
        "court": court,
        "form": form
    })

@staff_member_required
def approve_bookings(request):
    pending_bookings = Booking.objects.filter(status='pending').order_by('start_datetime')
    return render(request, 'bookings/approvebookings.html', {'bookings': pending_bookings})

@staff_member_required
def update_booking_status(request, booking_id, new_status):
    booking = Booking.objects.get(id=booking_id)
    booking.status = new_status
    booking.save()
    return redirect('bookings:approve_bookings')