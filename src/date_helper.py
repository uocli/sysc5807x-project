from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import traceback


class DateFormats(Enum):
    """
    Enum for date formats.
    """
    D_YYMMDD = "%y-%m-%d"
    D_DDMMyy = "%d-%m-%y"
    D_YYMMDD_N = "%y-%b-%d"
    D_DDMMyy_N = "%d-%b-%y"
    D_YYMMDDHHMMA_N = "%y-%b-%d, %I:%M%p"
    D_DDMMyyHHMMA_N = "%d-%b-%y, %I:%M%p"
    S_YYMMDD = "%y/%m/%d"
    S_DDMMyy = "%d/%m/%y"
    S_YYMMDDHHMMA = "%y/%m/%d, %I:%M%p"
    S_DDMMyyHHMMA = "%d/%m/%y, %I:%M%p"
    S_YYMMDDHHMMA_N = "%y/%b/%d, %I:%M%p"
    S_DDMMyyHHMMA_N = "%d/%b/%y, %I:%M%p"
    D_YYYYMMDD = "%Y-%m-%d"
    D_DDMMYYYY = "%d-%m-%Y"
    D_YYYYMMDDHHMMA = "%Y-%m-%d, %I:%M%p"
    D_DDMMYYYYHHMMA = "%d-%m-%Y, %I:%M%p"
    D_YYYYMMDD_N = "%Y-%b-%d"
    D_DDMMYYYY_N = "%d-%b-%Y"
    D_YYYYMMDDHHMMA_N = "%Y-%b-%d, %I:%M%p"
    D_DDMMYYYYHHMMA_N = "%d-%b-%Y, %I:%M%p"
    S_YYYYMMDD = "%Y/%m/%d"
    S_DDMMYYYY = "%d/%m/%Y"
    S_YYYYMMDDHHMMA = "%Y/%m/%d, %I:%M%p"
    S_DDMMYYYYHHMMA = "%d/%m/%Y, %I:%M%p"
    S_YYYYMMDDHHMMA_N = "%Y/%b/%d, %I:%M%p"
    S_DDMMYYYYHHMMA_N = "%d/%b/%Y, %I:%M%p"
    D_YYMMDDHHMMSSA_N = "%y-%b-%d, %I:%M:%S%p"
    D_DDMMyyHHMMSSA_N = "%d-%b-%y, %I:%M:%S%p"
    S_YYMMDDHHMMSSA = "%y/%m/%d, %I:%M:%S%p"
    S_DDMMyyHHMMSSA = "%d/%m/%y, %I:%M:%S%p"
    S_YYMMDDHHMMSSA_N = "%y/%b/%d, %I:%M:%S%p"
    S_DDMMyyHHMMSSA_N = "%d/%b/%y, %I:%M:%S%p"
    D_YYYYMMDDHHMMSSA = "%Y-%m-%d, %I:%M:%S%p"
    D_DDMMYYYYHHMMSSA = "%d-%m-%Y, %I:%M:%S%p"
    D_YYYYMMDDHHMMSSA_N = "%Y-%b-%d, %I:%M:%S%p"
    D_DDMMYYYYHHMMSSA_N = "%d-%b-%Y, %I:%M:%S%p"
    S_YYYYMMDDHHMMSSA = "%Y/%m/%d, %I:%M:%S%p"
    S_DDMMYYYYHHMMSSA = "%d/%m/%Y, %I:%M:%S%p"
    S_YYYYMMDDHHMMSSA_N = "%Y/%b/%d, %I:%M:%S%p"
    S_DDMMYYYYHHMMSSA_N = "%d/%b/%Y, %I:%M:%S%p"
    HHMMA = "%I:%M%p"
    HHMM = "%I:%M"
    HHMMSSA = "%I:%M:%S%p"
    HHMMSS = "%I:%M:%S"

    def get_date_format(self):
        """
        Returns the date format string.
        """
        return self.value


def prettify_date(timestamp: int) -> str:
    """
    Returns a prettified date string.
    If the date is today, returns time in "hh:mm a" format.
    Otherwise, returns date and time in "dd MMM hh:mm a" format.
    """
    date = datetime.fromtimestamp(timestamp / 1000)
    if date.date() == datetime.today().date():
        return date.strftime("%I:%M %p")
    else:
        return date.strftime("%d %b %I:%M %p")


def prettify_date_str(timestamp: str) -> str:
    """
    Returns a prettified date string.
    If the date is today, returns time in "hh:mm a" format.
    Otherwise, returns date and time in "dd MMM hh:mm a" format.
    """
    date = datetime.fromtimestamp(int(timestamp) / 1000)
    if date.date() == datetime.today().date():
        return date.strftime("%I:%M %p")
    else:
        return date.strftime("%d %b %I:%M %p")


def get_date_only_str(date: str) -> Optional[int]:
    """
    Parses a date string in "dd/MM/yyyy" format and returns the timestamp.
    """
    try:
        return int(datetime.strptime(date, "%d/%m/%Y").timestamp() * 1000)
    except ValueError:
        traceback.print_exc()
        return None


def get_date_only(timestamp: int) -> str:
    """
    Formats a timestamp into a date string in "dd/MM/yyyy" format.
    """
    return datetime.fromtimestamp(timestamp / 1000).strftime("%d/%m/%Y")


def get_date_and_time(timestamp: int) -> str:
    """
    Formats a timestamp into a date and time string in "dd/MM/yyyy, hh:mm a" format.
    """
    return datetime.fromtimestamp(timestamp / 1000).strftime("%d/%m/%Y, %I:%M %p")


def get_date_and_time_str(time: str) -> str:
    """
    Returns a formatted date and time string in "dd/MM/yyyy, hh:mm a" format.
    Accepts a timestamp as a string.
    """
    try:
        # Convert the string timestamp to an integer
        time_long = int(time)
        # Convert the timestamp to a datetime object
        date = datetime.fromtimestamp(time_long / 1000)
        # Format the date and time
        return date.strftime("%d/%m/%Y, %I:%M %p")  # dd/MM/yyyy, hh:mm a
    except ValueError:
        # Handle invalid input (e.g., non-numeric string)
        return "Invalid timestamp"


def get_time_only(timestamp: int) -> str:
    """
    Formats a timestamp into a time string in "hh:mm a" format.
    """
    return datetime.fromtimestamp(timestamp / 1000).strftime("%I:%M %p")


def get_today_with_time() -> str:
    """
    Returns today's date and time in "dd/MM/yyyy HH:mm:ss" format.
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def get_today() -> str:
    """
    Returns today's date in "dd/MM/yyyy" format.
    """
    return datetime.now().strftime("%d/%m/%Y")


def get_tomorrow() -> str:
    """
    Returns tomorrow's date in "dd/MM/yyyy" format.
    """
    return (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")


def get_days_between_two_dates(old: str, new_date: str, date_format: DateFormats) -> Optional[int]:
    """
    Calculates the number of days between two dates.
    Dates must be in the specified format.
    :param old: must be `dd/MM/yyyy, hh:mm a` format
    :param new_date: must be `dd/MM/yyyy, hh:mm a` format
    :param date_format: a member of DateFormats enum
    :return: number of days
    """
    try:
        date1 = datetime.strptime(old, date_format.get_date_format())
        date2 = datetime.strptime(new_date, date_format.get_date_format())
        delta = date1 - date2
        return delta.days
    except ValueError:
        traceback.print_exc()
        return None


def get_hours_between_two_dates(old: str, new_date: str, date_format: DateFormats) -> Optional[int]:
    """
    Calculates the number of hours between two dates.
    Dates must be in the specified format.
    :param old: must be `dd/MM/yyyy, hh:mm a` format
    :param new_date: must be `dd/MM/yyyy, hh:mm a` format
    :param date_format: a member of DateFormats enum
    :return: number of hours
    """
    try:
        date1 = datetime.strptime(old, date_format.get_date_format())
        date2 = datetime.strptime(new_date, date_format.get_date_format())
        delta = date1 - date2
        return int(delta.total_seconds() // 3600)
    except ValueError:
        traceback.print_exc()
        return None


def get_minutes_between_two_dates(old: str, new_date: str, date_format: DateFormats) -> Optional[int]:
    """
    Calculates the number of minutes between two dates.
    Dates must be in the specified format.
    :param old: must be `dd/MM/yyyy, hh:mm a` format
    :param new_date: must be `dd/MM/yyyy, hh:mm a` format
    :param date_format: a member of DateFormats enum
    :return: number of minutes
    """
    try:
        date1 = datetime.strptime(old, date_format.get_date_format())
        date2 = datetime.strptime(new_date, date_format.get_date_format())
        delta = date1 - date2
        return int(delta.total_seconds() // 60)
    except ValueError:
        traceback.print_exc()
        return None


def parse_any_date(date: str) -> Optional[int]:
    """
    Attempts to parse a date string using all available formats.
    Returns the timestamp if successful.
    :param date: the date string
    :return: the timestamp
    """
    for fmt in DateFormats:
        try:
            dt = datetime.strptime(date, fmt.get_date_format())
            return int(dt.timestamp() * 1000)
        except ValueError:
            traceback.print_exc()
            continue
    return None


def parse_date(date: str, date_format: DateFormats) -> Optional[int]:
    """
    Parses a date string using the specified format.
    Returns the timestamp if successful.
    :param date: the date string
    :param date_format: the date format
    :return: the timestamp
    """
    try:
        dt = datetime.strptime(date, date_format.get_date_format())
        return int(dt.timestamp() * 1000)
    except ValueError:
        traceback.print_exc()
        return 0


def get_desired_format(date_format: DateFormats, date: Optional[int] = None) -> str:
    """
    Formats a timestamp into the specified format.
    If no timestamp is provided, uses the current date and time.
    :param date_format: a member of DateFormats enum
    :param date: the timestamp
    :return: the formatted date string
    """
    dt = datetime.now() if date is None else datetime.fromtimestamp(date / 1000)
    return dt.strftime(date_format.get_date_format())


def get_date_from_days(num_of_days: int) -> str:
    """
    Returns the date after adding the specified number of days to today's date.
    The date is formatted in "dd-MMM-yy" format.
    :param num_of_days: the number of days to add
    :return: the formatted date string
    """
    dt = datetime.now() + timedelta(days=num_of_days)
    return dt.strftime(DateFormats.D_DDMMyy_N.get_date_format())


if __name__ == "__main__":
    print(prettify_date(int(datetime.now().timestamp() * 1000)))
    print(get_today())
    print(get_tomorrow())
    print(get_days_between_two_dates("01/01/2023", "02/01/2023", DateFormats.S_DDMMYYYY))
