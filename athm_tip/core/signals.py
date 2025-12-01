import logging

from django.dispatch import receiver

from django_athm.signals import (
    athm_cancelled_response,
    athm_completed_response,
    athm_expired_response,
)

logger = logging.getLogger(__name__)


@receiver(athm_completed_response)
def handle_completed(sender, transaction, **kwargs):
    logger.info(f"[demo] Payment completed: {transaction.reference_number}")


@receiver(athm_cancelled_response)
def handle_cancelled(sender, transaction, **kwargs):
    logger.info(f"[demo] Payment cancelled: {transaction.reference_number}")


@receiver(athm_expired_response)
def handle_expired(sender, transaction, **kwargs):
    logger.info(f"[demo] Payment expired: {transaction.reference_number}")
