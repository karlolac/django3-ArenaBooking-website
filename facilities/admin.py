from django.contrib import admin
from django import forms
from .models import Facility, Court

HOURS_CHOICES = [(f"{h:02d}:00:00", f"{h:02d}:00") for h in range(24)]

class FacilityAdminForm(forms.ModelForm):
    working_from = forms.ChoiceField(choices=HOURS_CHOICES, label="Radi od")
    working_till = forms.ChoiceField(choices=HOURS_CHOICES, label="Radi do")

    class Meta:
        model = Facility
        fields = '__all__'

@admin.register(Facility) 
class FacilityAdmin(admin.ModelAdmin):
    form = FacilityAdminForm
    list_display = ('name', 'city', 'working_from', 'working_till', 'is_active')
    list_editable = ('is_active',)

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility', 'sport', 'is_active')
    list_editable = ('is_active',)