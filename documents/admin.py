from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "category", "uploaded_by", "uploaded_at"]
    list_filter = ["category"]
    search_fields = ["title", "owner__username"]
