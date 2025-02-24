import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "la_mamadura.training"
    verbose_name = _("Training")

    def ready(self):
        with contextlib.suppress(ImportError):
            import la_mamadura.training.signals  # noqa: F401
