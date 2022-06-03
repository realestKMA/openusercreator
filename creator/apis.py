from rest_framework import status, views, viewsets, permissions, authentication
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from . import serializers, permissions as custom_perm, metadatas
from dj_rest_auth.jwt_auth import unset_jwt_cookies
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from .utils import Util
import jwt


# Custom user model instance
AppUser = get_user_model()


class AppUserApiView(viewsets.GenericViewSet):
    queryset = AppUser.objects.all()
    serializer_class = serializers.BasicAppUserSerializer()
    metadata_class = metadatas.AppMetadata

    def get_object(self, *args, **kwargs):
        """
        Edited so as to return the object instance of the currently logged in user.
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.request.user.username)

        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_staff:
            return serializers.FullAppUserSerializer
        return serializers.BasicAppUserSerializer

    def get_permissions(self, *args, **kwargs):
        if (self.action in ['create', 'api_schema']) or \
                str(reverse('creators_create', request=self.request)).endswith(self.request.path):
            permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [custom_perm.IsOwner & permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]

    def api_schema(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        return Response(data)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            # send email verification link
            Util.send_email_verification(data=serializer.data, request=request)

            return Response(data={"data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(data={"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), context={'request': request})
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data,
            context={'request': request},
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(data={"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        appuser = self.get_object()
        username, email, uid = appuser.username, appuser.email, appuser.uid
        data = {'data': {'username': username, 'email': email, 'uid': uid, 'detail': 'Deleted successfully'}}
        appuser.delete()
        response = Response(data=data, status=status.HTTP_204_NO_CONTENT)

        # clears jwt authentication if present
        unset_jwt_cookies(response)

        return response


class VerifyEmail(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')

        try:
            check_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return Response(
                data={"error": _('Activation link expired, please request a new one.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.DecodeError:
            return Response(
                data={"error": _('Invalid token, please request a new one.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user = AppUser.objects.get(id=check_token['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(data={"detail": _("Email address verified successfully")}, status=status.HTTP_200_OK)

            return Response(
                data={"detail": _("Your email address has already been verified")},
                status=status.HTTP_200_OK
            )


class ResendVerifyEmail(viewsets.GenericViewSet):
    serializer_class = serializers.ResendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            # check if email belongs to the currently logged in user.
            if request.user.email == serializer.data['email']:
                Util.resend_email_verification(data=serializer.data, request=request)
                return Response(data={"detaIl": _(F"A verification link has been sent to {serializer.data['email']}")})

            return Response(
                data={"error": _(F"Email address {serializer.data['email']} is not associated to your account")},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginSessionApiView(viewsets.GenericViewSet):
    """
    Login with username and password using django's (edited) built in authenticate and login functions.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )

            if user is not None:
                login(request, user)
                response = Response(data={"detail": _("Logged in successfully")}, status=status.HTTP_200_OK)

                # clear jwt (access & refresh) tokens if present
                unset_jwt_cookies(response)

                return response  # return logged in response to client

            return Response(data={"detail": _("wrong username/password")}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutSessionApiView(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(data={"detail": _("Logged out successfully")}, status=status.HTTP_200_OK)
