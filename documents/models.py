from django.conf import settings
from django.db import models


def upload_path(instance, filename):
    return f"documents/user_{instance.owner.id}/{filename}"


class Document(models.Model):
    CATEGORY_CHOICES = [
        ("tax", "Tax Filing"),
        ("sales_tax", "Sales Tax"),
        ("company", "Company Incorporation"),
        ("strn_ntn", "STRN & NTN"),
        ("bookkeeping", "Bookkeeping"),
        ("audit", "Audit"),
        ("secp_fbr_kpra", "SECP / FBR / KPRA"),
        ("other", "Other"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="documents", on_delete=models.CASCADE,
                               help_text="The client this document belongs to.")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="uploaded_documents",
                                     on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    file = models.FileField(upload_to=upload_path)
    note = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return self.file.name.split("/")[-1]
