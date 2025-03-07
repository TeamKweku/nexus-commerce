import logging
from typing import Any, Dict, Optional, Tuple

import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError
from social_core.backends.base import BaseAuth

from core_apps.profiles.models import Profile

logger = logging.getLogger(__name__)


def save_profile(
    backend: BaseAuth,
    user: Any,
    response: Dict[str, Any],
    *args: Any,
    **kwargs: Any,
) -> Optional[Tuple[Profile, bool]]:
    """
    Social auth pipeline to save user profile with Google OAuth avatar.

    Args:
        backend: Authentication backend being used
        user: User instance that was created/authenticated
        response: OAuth provider's response containing user info
        *args: Additional positional arguments
        **kwargs: Additional keyword arguments

    Returns:
        Optional[Tuple[Profile, bool]]: Tuple of (profile, created) if
        successful,
        None if no avatar update was needed

    Raises:
        CloudinaryError: If avatar upload to Cloudinary fails
    """
    if backend.name != "google-oauth2":
        return None

    avatar_url = response.get("picture")
    if not avatar_url:
        logger.debug("No avatar URL found in Google OAuth response")
        return None

    try:
        # Upload Google profile picture to Cloudinary
        upload_result = cloudinary.uploader.upload(
            avatar_url,
            folder="avatars",  # Organize uploads in a folder
            overwrite=True,  # Update existing avatar if any
        )

        # Get or create user profile
        profile, created = Profile.objects.get_or_create(user=user)

        # Save Cloudinary image ID to profile
        profile.avatar = upload_result["public_id"]
        profile.save()

        logger.info(
            "Successfully updated avatar for user %s (profile_id=%s)",
            user.username,
            profile.id,
        )

        return profile, created

    except CloudinaryError as e:
        logger.error(
            "Failed to upload avatar to Cloudinary for user %s: %s",
            user.username,
            str(e),
        )
        raise

    except Exception as e:
        logger.error(
            "Unexpected error while saving profile for user %s: %s",
            user.username,
            str(e),
        )
        raise
