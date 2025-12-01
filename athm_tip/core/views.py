from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django_athm.models import ATHM_Transaction
from django_athm.views import default_callback


def demo_page(request):
    """Django ATHM demo showcase page."""
    return render(request, "demo.html")


def tip_page(request):
    """Django ATHM tip showcase page."""
    # Handle status query params for toast messages
    status = request.GET.get("status")
    if status == "cancelled":
        messages.warning(request, "Payment was cancelled.")
    elif status == "expired":
        messages.error(request, "Payment session expired. Please try again.")

    context = {
        "ATHM_CONFIG": {
            "total": 3.00,
            "subtotal": 3.00,
            "tax": 0.00,
            "metadata_1": "Django ATHM Demo",
            "metadata_2": "Project Support Tip",
            "items": [
                {
                    "name": "Tip",
                    "description": "Support Django ATHM Development",
                    "quantity": "1",
                    "price": "3.00",
                    "tax": "0.00",
                    "metadata": "demo-tip",
                }
            ],
        }
    }
    return render(request, "tip.html", context)


@csrf_exempt
def athm_callback(request):
    """Custom callback that returns redirect info after processing."""
    # Call original callback for persistence + signals
    response = default_callback(request)

    # Extract status from request
    ecommerce_status = request.POST.get("ecommerceStatus", "")
    reference_number = request.POST.get("referenceNumber", "")

    # For intermediate statuses (OPEN, CONFIRM), return original response
    if ecommerce_status in ("OPEN", "CONFIRM"):
        return response

    # Determine redirect based on status
    if ecommerce_status == "COMPLETED":
        redirect_url = reverse("core:thank_you", args=[reference_number])
        status = "completed"
    elif ecommerce_status == "EXPIRED":
        redirect_url = f"{reverse('core:tip')}?status=expired"
        status = "expired"
    else:  # CANCEL, CANCELLED
        redirect_url = f"{reverse('core:tip')}?status=cancelled"
        status = "cancelled"

    return JsonResponse(
        {
            "status": status,
            "reference_number": reference_number,
            "redirect_url": redirect_url,
        }
    )


def thank_you(request, reference_number):
    """Display transaction details after successful payment."""
    transaction = get_object_or_404(ATHM_Transaction, reference_number=reference_number)
    return render(request, "thank_you.html", {"transaction": transaction})
