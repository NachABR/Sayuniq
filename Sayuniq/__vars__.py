import re
from datetime import datetime, timedelta, timezone

from decouple import config

from strings import get_string

# Version
__version__tuple__ = ("0", "0", "1")

__version__ = ".".join(__version__tuple__)
__version_short__ = ".".join(__version__tuple__[:-1])

#   # CONSTANTS
# Database 8 Restrictions
MONGO_URL = config("MONGO_URL", default=None)
AUTH_USERS = config("AUTH_USERS", default=None)
# Data
BOT_NAME = config("BOT_NAME", default="Sayuniq")
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
BOT_ALIAS = config("BOT_ALIAS", default="Sayuniq")
# Channels id
UTC = config("UTC", default="-6")
CHANNEL_ID = config("CHANNEL_ID", default=None)
LOG_CHANNEL = config("LOG_CHANNEL", default=None, cast=int)
TESTS_CHANNEL = config("TESTS_CHANNEL", default=None, cast=int)

# DATETIME
HOUR_FORMAT = 1 if config("HOUR_FORMAT", default=0, cast=int) == 24 else 0

# LOGGER
LOGGING_LEVEL = config("LOGGING_LEVEL", default="WARNING")

# SCRAPPER
USER_AGENT = {"user-agent": config("USER_AGENT", default=f"{BOT_ALIAS}/{__version__}")}


def human_hour_readable(hformat=HOUR_FORMAT, _utc=UTC):
    _hours, _minutes = UTC.split(":") if ":" in UTC else (UTC, 0)
    return datetime.now(timezone(timedelta(hours=int(_hours), minutes=int(_minutes)))).strftime(
        f"{get_string('format_date').format(datetime.now().month)} "
        f"{get_string('format_hour')[hformat]}")


def _channel_type(channel_id: str | int, thousand: bool = True):
    channel_id = str(channel_id) if isinstance(channel_id, int) else channel_id
    if not re.match(r"-?\d+", channel_id):
        return channel_id
    if thousand and str(-100) not in str(channel_id):
        return int(f'-100{channel_id}')
    elif thousand:
        return int(channel_id)
    else:
        return int(str(channel_id).replace("-100", ""))


def _base_channel_url(
        channel_id: str | int,
        message_id: str | int = None
):
    channel_id_filtered = _channel_type(channel_id, False)
    message_id = message_id or ""
    if isinstance(channel_id_filtered, int):
        return f"https://t.me/c/{channel_id_filtered}/{message_id}"
    else:
        return f"https://t.me/{channel_id_filtered}/{message_id}"


LOG_CHANNEL = _channel_type(LOG_CHANNEL)
TESTS_CHANNEL = _channel_type(TESTS_CHANNEL)
CHANNEL_ID = _channel_type(CHANNEL_ID)

