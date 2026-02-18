from django.shortcuts import render

def bookings(request):
    return render(request,'bookings.html')