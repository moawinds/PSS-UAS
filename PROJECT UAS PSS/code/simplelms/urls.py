"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from core import views
from core.api.api import api

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Django Allauth
    path("accounts/", include("allauth.urls")),

    # Smart Redirect
    path(
        "smart-redirect/",
        views.smart_login_redirect,
        name="smart_redirect",
    ),

    # Django Ninja REST API
    path("api/", api.urls),

    # Website LMS
    path("", include("core.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("silk/", include("silk.urls", namespace="silk")),
    ] + urlpatterns