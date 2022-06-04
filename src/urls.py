from django.views.generic import RedirectView
from dj_rest_auth import views as dj_rest
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),

    # redirect to the api urls.
    path('', RedirectView.as_view(url='api/creators/')),

    # api urls
    path('api/', include('creator.urls')),
    path(
        "api/auth/help/password/reset/",
        dj_rest.PasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "api/auth/help/password/reset/confirm/<str:uidb64>/<str:token>/",
        dj_rest.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
]
