from django import forms
from .models import Booking, Court
from datetime import datetime, timedelta

class BookingForm(forms.ModelForm):
    date_selection = forms.ChoiceField(
        label="1. Odaberite dan",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    time_selection = forms.ChoiceField(
        label="2. Odaberite vrijeme",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        # VAŽNO: NE stavljamo start_datetime ovdje
        fields = ["date_selection", "time_selection"]

    def __init__(self, *args, **kwargs):
        court_id = kwargs.pop('court_id', None)
        super().__init__(*args, **kwargs)

        date_choices = []
        time_choices = []

        if court_id:
            court = Court.objects.select_related('facility').get(id=court_id)
            f = court.facility
            today = datetime.now().date()

            dani_map = {
                'Monday': 'Ponedjeljak', 'Tuesday': 'Utorak', 'Wednesday': 'Srijeda',
                'Thursday': 'Četvrtak', 'Friday': 'Petak', 'Saturday': 'Subota', 'Sunday': 'Nedjelja'
            }

            for i in range(7):
                d = today + timedelta(days=i)
                hr_dan = dani_map.get(d.strftime('%A'), d.strftime('%A'))
                date_choices.append((d.strftime('%Y-%m-%d'), f"{d.strftime('%d.%m.')} ({hr_dan})"))

            for h in range(f.working_from.hour, f.working_till.hour):
                time_choices.append((f"{h:02d}:00", f"{h:02d}:00 - {h+1:02d}:00"))

        self.fields['date_selection'].choices = date_choices
        self.fields['time_selection'].choices = time_choices

    def clean(self):
        cleaned_data = super().clean()
        date_str = cleaned_data.get("date_selection")
        time_str = cleaned_data.get("time_selection")

        if date_str and time_str:
            start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

            if start_dt <= datetime.now():
                raise forms.ValidationError(
                    "Ne možete rezervirati termin koji je već prošao! Molimo odaberite kasniji termin ili drugi dan."
                )

            # spremi pravi datetime u cleaned_data pod ključem koji ćemo koristiti u save()
            cleaned_data["computed_start_datetime"] = start_dt

        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        start_dt = self.cleaned_data["computed_start_datetime"]
        obj.start_datetime = start_dt
        obj.end_datetime = start_dt + timedelta(hours=1)

        if commit:
            obj.save()
        return obj