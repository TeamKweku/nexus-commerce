import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _

# Get the active User model as defined in settings.AUTH_USER_MODEL
User = get_user_model()


class TimeStampedModel(models.Model):
    """
    An abstract base model that provides self-updating
    created and modified timestamps.
    """

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Model not created in database
        ordering = ["-created_at", "-updated_at"]


class ContentView(TimeStampedModel):
    """
    Tracks views/visits to any content type in the application.
    Uses Django's ContentTypes framework for generic relations.
    """

    # Generic foreign key fields for relating to any model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey("content_type", "object_id")

    # Optional link to user who viewed the content
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep view records even if user is deleted
        null=True,
        blank=True,
        related_name="content_views",
        verbose_name=_("User"),
    )

    # Store IP address for anonymous views and analytics
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("Viewer IP Address"), null=True, blank=True
    )
    # When the content was last viewed
    last_viewed = models.DateTimeField()

    class Meta:
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        # Ensure no duplicate views from same user/IP for same content
        unique_together = ["content_type", "object_id", "user", "viewer_ip"]

    def __str__(self) -> str:
        """
        String representation showing what was viewed by whom.
        """
        viewer = self.user.get_full_name if self.user else "Anonymous"
        return (
            f"{self.content_object} viewed by {viewer} "
            f"from IP {self.viewer_ip}"
        )

    @classmethod
    def record_view(
        cls, content_object: models.Model, user: "models.Model", viewer_ip: str
    ) -> None:
        """Record a view for a content object.

        Args:
            content_object: The Django model instance being viewed
            user: The user viewing the content
            viewer_ip: IP address of the viewer

        Returns:
            None

        Note:
            Silently handles integrity errors from duplicate views
            Uses get_or_create to prevent duplicate processing
        """
        content_type = ContentType.objects.get_for_model(content_object)
        try:
            view, created = cls.objects.get_or_create(
                content_type=content_type,
                object_id=content_object.pkid,
                defaults={"user": user, "viewer_ip": viewer_ip},
            )
            if not created:
                # View already exists, could update last_viewed here
                pass
        except IntegrityError:
            # Handle potential race conditions or constraint violations
            pass
