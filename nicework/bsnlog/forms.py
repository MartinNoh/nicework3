from django import forms
from .models import BslHistory


class BslHistoryForm(forms.ModelForm):
    class Meta:
        model = BslHistory
        fields = ['contents']