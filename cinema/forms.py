from datetime import date, time, datetime
from django import forms
from django.utils import timezone
from .models import Hall, Session, BookedSession


class HallForm(forms.ModelForm):
    class Meta:
        fields = ["name", "size"]
        model = Hall


class SessionForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if (start_date > end_date) or ((start_date == end_date) and (start_time >= end_time)) \
                or end_date < timezone.now().date():
            self.add_error("__all__", "Incorrect date")

    class Meta:
        fields = ["start_date", "end_date", "start_time", "end_time", "hall", "price"]
        model = Session


class BookedSessionForm(forms.ModelForm):

    class Meta:
        fields = ["session", "user", "date", "places"]
        model = BookedSession
        widgets = {
            "session": forms.HiddenInput(),
            "user": forms.HiddenInput(),
            "date": forms.HiddenInput(),
        }
