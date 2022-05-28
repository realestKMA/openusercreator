from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from django.urls import path
from . import apis


app_name = 'creator_app'

urlpatterns = [
    # auth urls
    path("auth/session/login/", apis.LoginApiView.as_view(), name="login-with-session"),
    path("auth/session/logout/", apis.LogoutApiView.as_view(), name="logout-with-session"),
    path("auth/token/", views.obtain_auth_token, name="Login-with-token"),
    
    
    path("creators/", apis.AppUserList.as_view({'get': 'list'}), name="creators-list"),
    path("creators/create/", apis.AppUserList.as_view({'post': 'create'}), name="creators-create"),
    path("creators/<str:username>/", apis.AppUserList.as_view({'get': 'retrieve'}), name="creators-details"),
    path("creators/<str:username>/update/", apis.AppUserList.as_view({'put': 'update', 'patch': 'update'}), name="creators-update"),
    path("creators/<str:username>/delete/", apis.AppUserList.as_view({'delete': 'destroy'}), name="creators-delete"),

]

format_suffix_patterns(urlpatterns, allowed=['json', 'xml'])