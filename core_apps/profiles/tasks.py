from uuid import UUID

import cloudinary.uploader
from celery import shared_task

from .models import Profile


@shared_task(name="upload_avatar_to_cloudinary")
def upload_avatar_to_cloudinary(profile_id: UUID, image_content: bytes) -> None:
    """
    Asynchronous task to upload user avatar images to Cloudinary.

    This task is executed in the background using Celery to prevent
    blocking the main application thread during image uploads.

    Args:
        profile_id: The unique identifier of the user's profile
        image_content: The binary content of the image to upload

    Returns:
        None

    Raises:
        Profile.DoesNotExist: If profile with given ID is not found
        cloudinary.Error: If upload to Cloudinary fails
    """
    profile = Profile.objects.get(id=profile_id)
    response = cloudinary.uploader.upload(image_content)
    profile.avatar = response["url"]
    profile.save()
