"""
This module provides keywords to support date time processing.
"""

from datetime import datetime, timezone, time
import platform
import pytz
from robot.api.deco import keyword
from robot.api import logger

TAG = 'datetime'
__all__ = [
    'get_now_datetime',
    'get_now_datetime_iso',
    'get_now_total_seconds',
    'get_current_date_with_local_timezone',
    'convert_epoch_to_date_and_time',
    'get_utc_datetime',
    'get_iso_datetime_tzcus',
    'get_iso_datetime_ml']

@keyword(name="Get Now UTC Datetime", tags=(TAG,))
def get_now_datetime() -> str:
    """
    Customize datetime format (Updated from get_current_date_with_local_timezone function).

    Example now datetime:

    2019-11-06T00:00:00.000+07:00

    Return type: string
    """
    try:
        th_now = get_current_date_with_local_timezone()
        th_now = str(th_now)
        return str(th_now)[0:23] + str(th_now)[26:32]
    except Exception as info:
        logger.error(f"{__name__} Can not get now datetime : {info}")
        raise


@keyword(name="Get Now ISO Datetime", tags=(TAG,))
def get_now_datetime_iso() -> str:
    """
    Get datetime ISO format.

    Example now datetime:

    2019-01-19T23:20:25.459Z

    Return type: string
    """
    try:
        now_dt = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return now_dt
    except Exception as info:
        logger.error(f"{__name__} Can not get now datetime iso : {info}")
        raise


@keyword(name="Get Now Total Seconds", tags=(TAG,))
def get_now_total_seconds() -> int:
    """
    Customize datetime format to total seconds form.

    Example now total seconds:

    1574628877

    Return type: string
    """
    try:
        total_sec = datetime.utcnow()
        total_sec = time.mktime(total_sec.timetuple())
        total_sec = int(total_sec)
        return total_sec
    except Exception as info:
        logger.error(f"{__name__} Can not get now total seconds : {info}")
        raise


@keyword(name="Get Current Date With Local Timezone", tags=(TAG,))
def get_current_date_with_local_timezone():
    """Get current date with local timezone with microsecond using ISO format.

    Example:

    | utc_dt = | Get Current Date With Local Timezone |

    =>

    | utc_dt = 2016-08-22T05:01:57.665221+07:00
    """
    try:
        utc_dt = datetime.now(timezone.utc)
        # Use tzlocal get_localzone
        utc_dt = format(utc_dt.astimezone(pytz.timezone('Asia/Bangkok')).isoformat())
        return utc_dt
    except Exception as e:
        logger.error('Get Current Date With Local Timezone method: ' + str(e))


@keyword(name="Convert Epoch To Datetime", tags=(TAG,))
def convert_epoch_to_date_and_time(epoch):
    """
    Convert from epoch to human-readable date with time zone in Bangkok.

    Supports Unix timestamps in seconds, milliseconds.

    The full set of format codes supported in https://strftime.org/.

    Examples:

    |                                                 | Input         | Output                   |
    | Assuming That This Timestamp Is In Milliseconds | 1575339570989 | Dec 3, 2019,  2:19:30 AM |
    | Assuming That This Timestamp Is In Seconds      | 1575339570    | Dec 3, 2019,  2:19:30 AM |
    """
    try:
        exp_date = None
        if len(str(epoch)) == 13:
            seconds = int(epoch) / 1000
        else:
            seconds = epoch
        # convert it to tz
        tz = pytz.timezone('Asia/Bangkok')
        # To check the operating system
        logger.debug("Detect platform: " + str(platform))
        if platform == "linux" or platform == "linux2":
            exp_date = datetime.fromtimestamp(seconds).astimezone(tz).strftime('%b %-d, %Y')
        elif platform == "win32" or platform == "win64":
            exp_date = datetime.fromtimestamp(seconds).astimezone(tz).strftime('%b %#d, %Y')
        exp_time = datetime.fromtimestamp(seconds).astimezone(tz).strftime('%I:%M:%S %p')
        return exp_date, exp_time
    except Exception as e:
        raise AssertionError("Convert Epoch To Date And Time: " + str(e))


@keyword(name="Get ISO_DATETIME_TZCUS", tags=(TAG,))
def get_iso_datetime_tzcus() -> str:
    """
    Custom datetime format (Update from get_current_date_with_local_timezone function).

    Example:
    2019-11-06T00:00:00+0700 (without ":" in timezone)

    """
    try:
        th_now = get_current_date_with_local_timezone()
        th_now = str(th_now)
        return str(th_now)[0:19] + str(th_now)[26:29] + str(th_now)[30:32]
    except Exception as info:
        logger.error(f"{__name__} Can not get now datetime : {info}")
        raise

@keyword(name="Get UTC Datetime", tags=(TAG,))
def get_utc_datetime() -> str:
    """
    Custom datetime format (Update from get_current_date_with_local_timezone function).

    Example:
    2019-11-06 00:00:00+07:00

    """
    try:
        th_now = get_current_date_with_local_timezone()
        th_now = str(th_now)
        return str(th_now)[0:10] + " " + str(th_now)[11:32]
    except Exception as info:
        logger.error(f"{__name__} Can not get now datetime : {info}")
        raise

@keyword(name="Get ISO_DATETIME_ML", tags=(TAG,))
def get_iso_datetime_ml() -> str:
    """
    Custom datetime format (Update from get_current_date_with_local_timezone function).

    Example:
    2020-07-02T11:55:13.914+07:00 (includes milisecond)

    """
    try:
        th_now = get_current_date_with_local_timezone()
        th_now = str(th_now)
        return str(th_now)[0:23] + str(th_now)[26:32]
    except Exception as info:
        logger.error(f"{__name__} Can not get now datetime : {info}")
        raise
