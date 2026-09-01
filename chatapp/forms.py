from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body", "attachment"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 2, "placeholder": "Type a message...", "class": "chat-input"}),
        }
