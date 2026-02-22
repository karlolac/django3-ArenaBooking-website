from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from facilities.models import Court
from .models import Booking
from .forms import BookingForm
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

@login_required
def bookings(request):
    if request.user.is_superuser:
        raise PermissionDenied("Admin nema pristup rezervacijama.")
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
       ## if request.user.is_superuser:
           ## messages.warning(request, "Admin može pregledati termine, ali ne može napraviti rezervaciju.")
           ## return redirect("bookings:bookcourt", court_id=court_id)

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

    return render(request, "bookings/bookcourt.html", {"court": court, "form": form})

@login_required
@permission_required("bookings.can_approve_booking", raise_exception=True)
def approve_bookings(request):
    if request.user.is_superuser:
       raise PermissionDenied("Superuser ne smije potvrđivati termine.")

    pending_bookings = Booking.objects.filter(status="pending").order_by("start_datetime")
    return render(request, "bookings/approvebookings.html", {"bookings": pending_bookings})


@login_required
@permission_required("bookings.can_approve_booking", raise_exception=True)
def update_booking_status(request, booking_id, new_status):
    if request.user.is_superuser:
        raise PermissionDenied("Superuser ne smije mijenjati status rezervacije.")

    booking = get_object_or_404(Booking, id=booking_id)

    if new_status not in ["confirmed", "cancelled"]:
        raise PermissionDenied("Nevažeći status.")

    booking.status = new_status
    booking.save()

    return redirect("bookings:approve_bookings")