import uuid
from typing import Any, Optional, Tuple, Union

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _

# Get the active User model as defined in settings.AUTH_USER_MODEL
User = get_user_model()


class TimeStampedModel(models.Model):
    """
    An abstract base model that provides self-updating created
    and modified timestamps.

    Attributes:
        pkid: Big integer primary key
        id: UUID-based unique identifier
        created_at: Timestamp of instance creation
        updated_at: Timestamp of last update
    """

    pkid: models.BigAutoField = models.BigAutoField(
        primary_key=True, editable=False
    )
    id: models.UUIDField = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Model not created in database
        ordering = ["-created_at", "-updated_at"]


class ContentView(TimeStampedModel):
    """
    Tracks views/visits to any content type in the application.
    Uses Django's ContentTypes framework for generic relations.

    Attributes:
        content_type: Foreign key to ContentType model
        object_id: ID of the viewed object
        content_object: Generic foreign key to the viewed content
        user: Optional foreign key to the user who viewed the content
        viewer_ip: IP address of the viewer
        last_viewed: Timestamp of the last view
    """

    content_type: models.ForeignKey = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type")
    )
    object_id: models.PositiveIntegerField = models.PositiveIntegerField(
        verbose_name=_("Object ID")
    )
    content_object: GenericForeignKey = GenericForeignKey(
        "content_type", "object_id"
    )

    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep view records even if user is deleted
        null=True,
        blank=True,
        related_name="content_views",
        verbose_name=_("User"),
    )

    viewer_ip: models.GenericIPAddressField = models.GenericIPAddressField(
        verbose_name=_("Viewer IP Address"), null=True, blank=True
    )
    last_viewed: models.DateTimeField = models.DateTimeField()

    class Meta:
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        unique_together = ["content_type", "object_id", "user", "viewer_ip"]

    def __str__(self) -> str:
        """
        String representation showing what was viewed by whom.

        Returns:
            str: Formatted string with content, viewer, and IP information
        """
        viewer: Union[str, Any] = (
            self.user.get_full_name if self.user else "Anonymous"
        )
        return (
            f"{self.content_object} viewed by {viewer} from IP {self.viewer_ip}"
        )

    @classmethod
    def record_view(
        cls,
        content_object: models.Model,
        user: Optional[models.Model],
        viewer_ip: str,
    ) -> None:
        """
        Record a view for a content object.

        Args:
            content_object: The Django model instance being viewed
            user: The user viewing the content (can be None for anonymous views)
            viewer_ip: IP address of the viewer

        Returns:
            None

        Note:
            Silently handles integrity errors from duplicate views
            Uses get_or_create to prevent duplicate processing
        """
        content_type: ContentType = ContentType.objects.get_for_model(
            content_object
        )
        try:
            view: Tuple[ContentView, bool] = cls.objects.get_or_create(
                content_type=content_type,
                object_id=content_object.pkid,
                defaults={"user": user, "viewer_ip": viewer_ip},
            )
            if not view[1]:  # if not created
                # View already exists, could update last_viewed here
                pass
        except IntegrityError:
            # Handle potential race conditions or constraint violations
            pass
