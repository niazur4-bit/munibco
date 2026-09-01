from django.contrib import admin
from .models import ServiceRecord


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ["client", "service_type", "amount", "status", "month"]
    list_filter = ["service_type", "status"]
