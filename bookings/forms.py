from django import forms
from .models import Booking, Court
from datetime import datetime, timedelta, time

class BookingForm(forms.ModelForm):
    date_selection = forms.ChoiceField(
        label="1. Odaberite dan",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_datetime = forms.ChoiceField(
        label="2. Odaberite vrijeme",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ["date_selection", "start_datetime"]

    def __init__(self, *args, **kwargs):
        court_id = kwargs.pop('court_id', None)
        super().__init__(*args, **kwargs)
        
        date_choices = []
        time_choices = []
        
        if court_id:
            try:
                court = Court.objects.select_related('facility').get(id=court_id)
                f = court.facility
                today = datetime.now().date()

                for i in range(7):
                    d = today + timedelta(days=i)
                    date_choices.append((d.strftime('%Y-%m-%d'), d.strftime('%d.%m. (%A)')))

                for h in range(f.working_from.hour, f.working_till.hour):
                    time_choices.append((f"{h:02d}:00", f"{h:02d}:00 - {h+1:02d}:00"))
                
            except Exception as e:
                print(f"Greška: {e}")

        self.fields['date_selection'].choices = date_choices
        self.fields['start_datetime'].choices = time_choices

    def clean(self):
        cleaned_data = super().clean()
        date_str = cleaned_data.get("date_selection")
        time_str = cleaned_data.get("start_datetime")

        if date_str and time_str:
            combined_str = f"{date_str} {time_str}"
            cleaned_data["start_datetime"] = datetime.strptime(combined_str, '%Y-%m-%d %H:%M')
        
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.start_datetime = self.cleaned_data["start_datetime"]
        obj.end_datetime = obj.start_datetime + timedelta(hours=1)
        
        if commit:
            obj.save()
        return obj