from decimal import Decimal

from django.shortcuts import render


def get_athm_config(amount):
    """Generate ATHM config for a given amount."""
    amount_str = f"{amount:.2f}"
    return {
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
