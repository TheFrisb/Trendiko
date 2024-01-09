from datetime import datetime

from django.conf import settings
from django.utils import timezone


def make_timezone_aware(date_obj):
    """Convert a date object to a timezone-aware datetime object."""
    print(date_obj)
    if isinstance(date_obj, datetime):
        dt = date_obj
    else:
        # Convert date object to a datetime object at the beginning of the day
        dt = datetime.combine(date_obj, datetime.min.time())

    if timezone.is_naive(dt):
        tz = timezone.get_default_timezone() if settings.USE_TZ else timezone.utc
        return timezone.make_aware(dt, tz)
    return dt
