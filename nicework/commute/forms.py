from django import forms
from .models import CmtHistory


class CmtHistoryForm(forms.ModelForm):
    class Meta:
        model = CmtHistory
        fields = ['startdatetime', 'enddatetime', 'notice']