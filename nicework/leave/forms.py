from django import forms
from .models import LevHistory


class LevHistoryForm(forms.ModelForm):
    class Meta:
        model = LevHistory
        fields = ['reason', 'startdate', 'enddate', 'leavecat', 'starttime', 'endtime', 'emgnum']