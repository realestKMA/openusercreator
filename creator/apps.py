from django.db.models.signals import post_save
from django.apps import AppConfig
from django.conf import settings
import uuid


class CreatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'creator'

    def ready(self) -> None:
        from . import signals
        from . import models

        post_save.connect(signals.new_creator, sender=settings.AUTH_USER_MODEL, dispatch_uid=uuid.uuid4())
        post_save.connect(signals.new_openuserapp, sender=models.Openuser, dispatch_uid=uuid.uuid4())
