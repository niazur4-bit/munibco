from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ContactForm

SERVICES = [
    {"icon": "check-square", "title": "Income Tax Filing",
     "desc": "Timely and accurate filing of Income Tax Returns for Individuals, AOPs and Companies."},
    {"icon": "percent", "title": "Sales Tax Filing",
     "desc": "Sales Tax Registration, Returns and Compliance to keep your business fully compliant."},
    {"icon": "building", "title": "Company Incorporation",
     "desc": "Complete assistance in company registration and incorporation with SECP."},
    {"icon": "id-card", "title": "STRN & NTN Preparation",
     "desc": "Preparation and registration of Sales Tax Registration Number (STRN) and National Tax Number (NTN)."},
    {"icon": "book-open", "title": "Bookkeeping",
     "desc": "Accurate and organized bookkeeping services to keep your financial records up to date."},
    {"icon": "search", "title": "Internal & External Audit Services",
     "desc": "Independent and objective audit services to ensure compliance and enhance your business value."},
    {"icon": "landmark", "title": "SECP, FBR & KPRA Related Services",
     "desc": "Professional assistance in all regulatory matters related to SECP, FBR and KPRA."},
]

WHY_CHOOSE_US = [
    "Experienced & Qualified Professionals",
    "Up-to-date with Latest Laws & Regulations",
    "Timely Delivery & Quality Assurance",
    "Confidential & Reliable Services",
    "Client Focused Approach",
]


def home(request):
    return render(request, "core/home.html", {"services": SERVICES, "why_choose_us": WHY_CHOOSE_US})


def services(request):
    return render(request, "core/services.html", {"services": SERVICES})


def about(request):
    return render(request, "core/about.html", {"why_choose_us": WHY_CHOOSE_US})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received. We'll get back to you shortly.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})
