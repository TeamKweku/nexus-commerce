from django.urls import path

from .views import (
    AvatarUploadView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileUpdateAPIView,
    PublicProfileDetailAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="profiles"),
    path(
        "<slug:slug>/",
        PublicProfileDetailAPIView.as_view(),
        name="public-profile",
    ),
    path(
        "user/my-profile/",
        ProfileDetailAPIView.as_view(),
        name="profile-detail",
    ),
    path("user/update/", ProfileUpdateAPIView.as_view(), name="profile-update"),
    path("user/avatar/", AvatarUploadView.as_view(), name="avatar-upload"),
]
