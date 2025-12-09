from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from django_athm.models import Payment, WebhookEvent


def tip_page(request):
    """Django ATHM tip showcase page."""
    # Handle status query params for toast messages
    status = request.GET.get("status")
    if status == "cancelled":
        messages.warning(request, _("Payment was cancelled."))
    elif status == "expired":
        messages.error(request, _("Payment session expired. Please try again."))

    # Get current language for ATH Móvil button
    current_lang = get_language()
    athm_lang = "es" if current_lang == "es" else "en"

    context = {
        "ATHM_CONFIG": {
            "total": 3.00,
            "subtotal": 3.00,
            "tax": 0.00,
            "metadata_1": str(_("Django ATHM Demo")),
            "metadata_2": str(_("Project Support Tip")),
            "theme": "btn",
            "lang": athm_lang,
            "items": [
                {
                    "name": str(_("Tip")),
                    "description": str(_("Support Django ATHM Development")),
                    "quantity": "1",
                    "price": "3.00",
                    "tax": "0.00",
                    "metadata": "demo-tip",
                }
            ],
            "success_url": request.build_absolute_uri(reverse("core:thank_you")),
            "failure_url": request.build_absolute_uri(
                reverse("core:tip") + "?status=cancelled"
            ),
        }
    }
    return render(request, "tip.html", context)


def thank_you(request):
    """Display transaction details after successful payment."""
    reference_number = request.GET.get("reference_number")
    if not reference_number:
        messages.error(request, _("Missing payment reference."))
        return render(
            request, "thank_you.html", {"payment": None, "webhook_events": []}
        )

    payment = get_object_or_404(Payment, reference_number=reference_number)

    # Get webhook events for this payment
    webhook_events = WebhookEvent.objects.filter(transaction=payment).order_by(
        "-created"
    )

    context = {
        "payment": payment,
        "webhook_events": webhook_events,
    }
    return render(request, "thank_you.html", context)
