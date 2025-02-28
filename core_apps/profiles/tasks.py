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
        profile_id (UUID): The unique identifier of the user's profile
        image_content (bytes): The binary content of the image to upload

    Returns:
        None

    Process:
        1. Retrieves the profile instance using the provided ID
        2. Uploads the image content to Cloudinary
        3. Updates the profile's avatar URL with the Cloudinary response
        4. Saves the updated profile

    Note:
        The @shared_task decorator makes this task available to any part
        of the application that needs to handle avatar uploads.
    """

    profile = Profile.objects.get(id=profile_id)
    response = cloudinary.uploader.upload(image_content)
    profile.avatar = response["url"]
    profile.save()
