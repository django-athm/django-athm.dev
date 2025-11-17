from django.shortcuts import render
from decimal import Decimal


def landing(request):
    """Landing page view."""
    return render(request, "landing.html")


def get_athm_config(amount):
    """Generate ATHM config for a given amount."""
    amount_str = f"{amount:.2f}"
    return {
        "theme": "btn",
        "language": "en",
        "total": float(amount),
        "subtotal": float(amount),
        "tax": 0.00,
        "metadata_1": "Django ATHM Demo",
        "metadata_2": "Tip Showcase",
        "items": [
            {
                "name": "Tip",
                "description": "Support Django ATHM Development",
                "quantity": "1",
                "price": amount_str,
                "tax": "0.00",
                "metadata": "demo-tip",
            }
        ],
    }


def tip_page(request):
    """Django ATHM tip showcase page."""
    context = {"ATHM_CONFIG": get_athm_config(Decimal("5.00"))}
    return render(request, "tip.html", context)


def update_athm_button(request):
    """HTMX endpoint to update the ATHM button with new amount."""
    amount = request.GET.get("selected-amount-value", "5.00")
    try:
        amount = Decimal(amount)
        if amount <= 0:
            amount = Decimal("5.00")
    except (ValueError, TypeError):
        amount = Decimal("5.00")

    context = {"ATHM_CONFIG": get_athm_config(amount)}
    return render(request, "partials/athm_button.html", context)
