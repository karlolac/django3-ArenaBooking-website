from django.shortcuts import render
from facilities.models import Facility


def facilities(request):
    facilities=Facility.objects.all()
    return render(request,'facilities/facilities.html',{'facilities':facilities})

from django.shortcuts import render, get_object_or_404
from .models import Facility

def facilitydetail(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    courts = facility.courts.filter(is_active=True)
    return render(request, 'facilities/facilitydetail.html', {
        'facility': facility,
        'courts':courts
        })
