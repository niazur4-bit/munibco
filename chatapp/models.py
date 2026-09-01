from django.conf import settings
from django.db import models


def attachment_path(instance, filename):
    return f"chat_attachments/{instance.sender.id}/{filename}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    attachment = models.FileField(upload_to=attachment_path, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.body[:30]}"
