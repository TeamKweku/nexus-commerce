import cloudinary.uploader

from core_apps.profiles.models import Profile


def save_profile(backend, user, response, *args, **kwargs):
    """
    Social auth pipeline to save user profile with Google OAuth avatar.

    Args:
        backend: Authentication backend being used
        user: User instance that was created/authenticated
        response: OAuth provider's response containing user info

    Handles:
        - Google OAuth2 authentication
        - Avatar image upload to Cloudinary
        - Profile creation/update with avatar
    """
    if backend.name == "google-oauth2":
        avatar_url = response.get("picture", None)
        if avatar_url:
            # Upload Google profile picture to Cloudinary
            upload_result = cloudinary.uploader.upload(avatar_url)
            # Get or create user profile
            profile, created = Profile.objects.get_or_create(user=user)
            # Save Cloudinary image ID to profile
            profile.avatar = upload_result["public_id"]
            profile.save()
