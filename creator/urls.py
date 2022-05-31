from dj_rest_auth.registration import views as dj_rest_reg, urls
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth import views as dj_rest
from django.urls import path
from . import apis

app_name = 'creator_app'


urlpatterns = [
    # auth urls
    path("auth/login/token/", dj_rest.LoginView.as_view(), name="login_via_token"),
    path("auth/logout/token/", dj_rest.LogoutView.as_view(), name="logout_via_token"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("auth/login/session/", apis.LoginApiView.as_view(), name="login_via_session"),
    path("auth/logout/session/", apis.LogoutApiView.as_view(), name="logout_with_session"),

    # reset password via email urls
    path("auth/help/password/reset/", dj_rest.PasswordResetView.as_view(), name="reset_password"),
    path("auth/help/password/reset/confirm/", dj_rest.PasswordResetConfirmView.as_view(), name="reset_password_confirm"),

    # create new account urls
    path("creators/new/", apis.AppUserList.as_view({'post': 'create'}), name="creators_create"),
    path("creators/new/verify-email/", apis.VerifyEmail.as_view(), name="creators_verify_email"),
    # path("creators/new/resend-email/", dj_rest_reg.ResendEmailVerificationView.as_view(), name="creators_resend_email"),

    # creators list and object instance
    path("creators/", apis.AppUserList.as_view({'get': 'list'}), name="creators_list"),
    path("creators/me/", apis.AppUserList.as_view({'get': 'retrieve'}), name="creators_details"),
    path("creators/me/update/", apis.AppUserList.as_view({'put': 'update', 'patch': 'update'}), name="creators_update"),
    path("creators/me/delete/", apis.AppUserList.as_view({'delete': 'destroy'}), name="creators_delete"),

    # change authenticated creators password url
    path("creators/me/password/change/", dj_rest.PasswordChangeView.as_view(), name="change_password"),
]
