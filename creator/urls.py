from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import apis


app_name = 'creator_app'

urlpatterns = [
    path("creators/", apis.AppUserList.as_view({'get': 'list'}), name="creators-list"),
    path("creators/create/", apis.AppUserList.as_view({'post': 'create'}), name="creators-create"),
    path("creators/<str:username>/", apis.AppUserList.as_view({'get': 'retrieve'}), name="creators-details"),
    path("creators/<str:username>/update/", apis.AppUserList.as_view({'put': 'update', 'patch': 'update'}), name="creators-update"),
    path("creators/<str:username>/delete/", apis.AppUserList.as_view({'delete': 'destroy'}), name="creators-delete"),
]

format_suffix_patterns(urlpatterns, allowed=['json', 'yaml', 'xml'])