from django import forms
from .models import Document


class ClientDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "category", "file", "note"]


class AdminDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["owner", "title", "category", "file", "note"]
