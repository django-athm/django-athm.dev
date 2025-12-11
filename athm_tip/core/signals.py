import logging

from django.core.mail import mail_admins
from django.dispatch import receiver
from django.utils import timezone
from django_athm.signals import (
    payment_cancelled,
    payment_completed,
    payment_expired,
    refund_sent,
)

logger = logging.getLogger(__name__)


@receiver(payment_completed)
def handle_completed(sender, payment, **kwargs):
    """Log comprehensive payment completion details with webhook-enriched data."""
    customer_name = payment.customer_name or "N/A"
    customer_phone = payment.customer_phone or "N/A"

    logger.info(
        f"[COMPLETED] Payment {payment.reference_number} | "
        f"ID: {payment.ecommerce_id} | "
        f"Total: ${payment.total} (Subtotal: ${payment.subtotal}, Tax: ${payment.tax}) | "
        f"Fee: ${payment.fee}, Net: ${payment.net_amount} | "
        f"Items: {payment.items.count()} | "
        f"Customer: {customer_name[0] if customer_name != 'N/A' else 'N/A'}*** "
        f"(Phone: ***{customer_phone[-4:] if len(customer_phone) >= 4 else customer_phone}) | "
        f"Transaction Date: {payment.transaction_date or payment.created_at}"
    )


@receiver(payment_completed)
def notify_admins(sender, payment, **kwargs):
    """Send email notification to admins with full payment details."""
    subject = f"New Payment: ${payment.total} - {payment.reference_number}"

    items_list = payment.items.all()
    items_text = "\n".join(
        [
            f"  - {item.name}: ${item.price} x {item.quantity} = ${item.price * item.quantity}"
            for item in items_list
        ]
    )

    message = f"""New payment completed via django-athm:

Reference: {payment.reference_number}
Ecommerce ID: {payment.ecommerce_id}
Status: {payment.status}

Amounts:
- Total: ${payment.total}
- Subtotal: ${payment.subtotal}
- Tax: ${payment.tax}
- Fee: ${payment.fee}
- Net Amount: ${payment.net_amount}

Customer:
- Name: {payment.customer_name or "N/A"}
- Phone: {payment.customer_phone or "N/A"}
- Email: {payment.customer_email or "N/A"}

Line Items ({items_list.count()}):
{items_text or "  (none)"}

Metadata:
- metadata_1: {payment.metadata_1 or "N/A"}
- metadata_2: {payment.metadata_2 or "N/A"}

Transaction Date: {payment.transaction_date or payment.created_at}
Created: {payment.created_at}
"""

    mail_admins(subject, message)


@receiver(payment_cancelled)
def handle_cancelled(sender, payment, **kwargs):
    """Log payment cancellation with duration analysis."""
    duration = timezone.now() - payment.created_at

    logger.info(
        f"[FAILED] Payment {payment.reference_number or payment.ecommerce_id} | "
        f"ID: {payment.ecommerce_id} | "
        f"Total: ${payment.total} | "
        f"Items: {payment.items.count()} | "
        f"Duration: {duration.total_seconds():.1f}s | "
        f"Created: {payment.created_at}"
    )


@receiver(payment_expired)
def handle_expired(sender, payment, **kwargs):
    """Log payment expiration with duration analysis."""
    duration = timezone.now() - payment.created_at

    logger.info(
        f"[EXPIRED] Payment {payment.reference_number or payment.ecommerce_id} | "
        f"ID: {payment.ecommerce_id} | "
        f"Total: ${payment.total} | "
        f"Items: {payment.items.count()} | "
        f"Duration: {duration.total_seconds():.1f}s | "
        f"Created: {payment.created_at}"
    )


@receiver(refund_sent)
def handle_refund(sender, refund, **kwargs):
    """Log refund completion with remaining refundable balance."""
    payment = refund.payment

    logger.info(
        f"[REFUND] Refund {refund.transaction_id} | "
        f"Payment: {payment.reference_number} | "
        f"Refund Amount: ${refund.amount} | "
        f"Original Total: ${payment.total} | "
        f"Total Refunded: ${payment.total_refunded_amount} | "
        f"Refundable Balance: ${payment.refundable_amount} | "
        f"Refund Date: {refund.created_at}"
    )
