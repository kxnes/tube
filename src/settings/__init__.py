from django.core.exceptions import ImproperlyConfigured

from .common import *

try:
    from .local import *
except ImportError as exc:
    raise ImproperlyConfigured(
        'Local settings is not configured. '
        'Please, check `local.py` module.'
    ) from exc
