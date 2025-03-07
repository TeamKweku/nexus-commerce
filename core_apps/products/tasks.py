from celery import shared_task
from django.core.mail import send_mail

from .models import ProductLine


@shared_task(name="check_low_stock_levels")
def check_low_stock_levels():
    """
    Daily check for products with low stock levels.
    Notifies administrators when stock falls below threshold.
    """
    low_stock_threshold = 5
    low_stock_items = ProductLine.objects.filter(
        stock_qty__lte=low_stock_threshold
    )

    if low_stock_items.exists():
        message = "Low stock alert for:\n"
        for item in low_stock_items:
            message += (
                f"- {item.product.name} "
                f"(SKU: {item.sku}): "
                f"{item.stock_qty} remaining\n"
            )

        send_mail(
            subject="Low Stock Alert",
            message=message,
            from_email="system@nexuscommerce.com",
            recipient_list=["admin@nexuscommerce.com"],
        )
