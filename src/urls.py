from django.views.generic import RedirectView
from django.conf.urls.static import static
from dj_rest_auth import views as dj_rest
from django.urls import path, include
from creator.admin import admin_site
# from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path('admin/', admin_site.urls),

    # redirect to the api urls.
    path('', RedirectView.as_view(url='api/v1/')),

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

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
