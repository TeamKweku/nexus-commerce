from typing import List

from celery import shared_task
from django.core.mail import send_mail
from django.db.models.query import QuerySet

from .models import ProductLine


@shared_task(
    name="check_low_stock_levels",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def check_low_stock_levels() -> None:
    """
    Daily check for products with low stock levels.
    Notifies administrators when stock falls below threshold.

    This task:
    1. Queries all product lines with stock quantity <= threshold
    2. Generates a formatted message with low stock items
    3. Sends email notification to administrators

    Note:
        - Configured to retry up to 3 times with exponential backoff
        - Threshold is currently set to 5 units
        - Email is sent only if low stock items are found

    Returns:
        None: This task doesn't return any value

    Raises:
        Exception: Any exceptions during execution will trigger retry mechanism
    """
    low_stock_threshold: int = 5
    low_stock_items: QuerySet[ProductLine] = ProductLine.objects.filter(
        stock_qty__lte=low_stock_threshold
    )

    if low_stock_items.exists():
        message: str = "Low stock alert for:\n"
        for item in low_stock_items:
            message += (
                f"- {item.product.name} "
                f"(SKU: {item.sku}): "
                f"{item.stock_qty} remaining\n"
            )

        recipient_list: List[str] = ["admin@nexuscommerce.com"]
        send_mail(
            subject="Low Stock Alert",
            message=message,
            from_email="system@nexuscommerce.com",
            recipient_list=recipient_list,
            fail_silently=False,
        )
