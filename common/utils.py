import logging
from datetime import datetime, timedelta

import pytz
import requests
from django.conf import settings
from django.utils import timezone


def make_timezone_aware(date_obj):
    """Convert a date object to a timezone-aware datetime object."""
    if isinstance(date_obj, datetime):
        dt = date_obj
    else:
        dt = datetime.combine(date_obj, datetime.min.time())

    if timezone.is_naive(dt):
        tz = timezone.get_default_timezone() if settings.USE_TZ else timezone.utc

        return timezone.make_aware(dt, tz)

    return dt


def get_macedonian_month(month):
    # Dictionary mapping English month names to Macedonian Cyrillic
    macedonian_months = {
        "January": "Јануари",
        "February": "Февруари",
        "March": "Март",
        "April": "Април",
        "May": "Мај",
        "June": "Јуни",
        "July": "Јули",
        "August": "Август",
        "September": "Септември",
        "October": "Октомври",
        "November": "Ноември",
        "December": "Декември",
    }
    return macedonian_months.get(month, month)


def get_macedonian_day(day):
    # Dictionary mapping English day names to Macedonian Cyrillic
    macedonian_days = {
        "Monday": "Понеделник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четврток",
        "Friday": "Петок",
        "Saturday": "Сабота",
        "Sunday": "Недела",
    }
    return macedonian_days.get(day, day)


def convert_to_cest(utc_time):
    """Convert a UTC time to CEST time."""
    utc_timezone = pytz.timezone("UTC")
    cest_timezone = pytz.timezone("Europe/Skopje")
    utc_time = utc_timezone.localize(utc_time)
    cest_time = utc_time.astimezone(cest_timezone)
    return cest_time


def calculate_delivery_dates(current_day=None):
    if current_day is None:
        current_time_cest = convert_to_cest(datetime.now())
        current_day = current_time_cest.strftime("%A")

    delivery_intervals = {
        "Monday": (2, 4),
        "Tuesday": (2, 4),
        "Wednesday": (2, 5),
        "Thursday": (2, 4),
        "Friday": (3, 4),
        "Saturday": (2, 4),
        "Sunday": (2, 4),
    }

    # Get the current date
    today = datetime.now()

    # Calculate the delivery interval
    start_offset, end_offset = delivery_intervals[current_day]

    # Calculate the expected delivery dates
    start_delivery_date = today + timedelta(days=start_offset)
    end_delivery_date = today + timedelta(days=end_offset)

    # Format the dates
    start_month = get_macedonian_month(start_delivery_date.strftime("%B"))
    end_month = get_macedonian_month(end_delivery_date.strftime("%B"))
    start_day = get_macedonian_day(start_delivery_date.strftime("%A"))
    end_day = get_macedonian_day(end_delivery_date.strftime("%A"))

    return {
        "start_day": start_day,
        "end_day": end_day,
        "start_month_formatted": f"{start_delivery_date.day} {start_month[:3]}.",
        "end_month_formatted": f"{end_delivery_date.day} {end_month[:3]}.",
    }


def get_ip_addr(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", None)

    if ip is None:
        ip = "None"
    return ip


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT", "None")


def get_euro_value_in_mkd(exchange_rate=None, value=1):
    if exchange_rate is None:
        response = requests.get(
            f"https://api.exchangerate-api.com/v6/{settings.EXCHANGE_RATE_API_KEY}/latest/EUR"
        )

        try:
            data = response.json()
            exchange_rate = data["rates"]["MKD"]
        except Exception as e:
            logging.error("Error fetching exchange rate data: %s", e)
            exchange_rate = 61.58

    return float(value * exchange_rate)
