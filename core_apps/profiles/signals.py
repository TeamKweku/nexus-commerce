import logging
from typing import Any, Type

from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from config.settings.base import AUTH_USER_MODEL
from core_apps.profiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Type[Model], instance: Model, created: bool, **kwargs: Any
) -> None:
    """
    Create profile for new users or log status for existing ones.

    Automatically triggered after a user instance is saved. Creates a new
    profile for new users or logs status for existing users.

    Args:
        sender: Model class that sent the signal (User model)
        instance: Actual user instance that was saved
        created: Boolean indicating if this is a new user
        **kwargs: Additional signal arguments

    Returns:
        None
    """
    if created:
        Profile.objects.create(user=instance)
        logger.info(
            f"Profile created for {instance.first_name} {instance.last_name}"
        )
    else:
        logger.info(
            f"Profile already exists for "
            f"{instance.first_name} {instance.last_name}"
        )
