from django import forms
from .models import ServiceRecord


class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ["client", "service_type", "amount", "status", "month"]
        widgets = {"month": forms.DateInput(attrs={"type": "date"})}
