from django.conf import settings
from django.db import models


class ServiceRecord(models.Model):
    """A billable service engagement used to drive the analytics dashboards."""
    SERVICE_CHOICES = [
        ("income_tax", "Income Tax Filing"),
        ("sales_tax", "Sales Tax Filing"),
        ("company_inc", "Company Incorporation"),
        ("strn_ntn", "STRN & NTN Preparation"),
        ("bookkeeping", "Bookkeeping"),
        ("audit", "Internal & External Audit"),
        ("secp_fbr_kpra", "SECP, FBR & KPRA Related"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="service_records", on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    month = models.DateField(help_text="Use the 1st of the billing month")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_records",
                                    on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-month"]

    def __str__(self):
        return f"{self.client} - {self.get_service_type_display()} - {self.month}"
