import re
from datetime import datetime, timedelta, timezone

from freezegun import freeze_time
import pytest

from date_format_converter import (
    DateFormats,
    prettify_date,
    prettify_date_str,
    get_date_only_str,
    get_date_only,
    get_date_and_time,
    get_date_and_time_str,
    get_time_only,
    get_today_with_time,
    get_today,
    get_tomorrow,
    get_days_between_two_dates,
    get_hours_between_two_dates,
    get_minutes_between_two_dates,
    parse_any_date,
    parse_date,
    get_desired_format,
    get_date_from_days,
    date_picker_dialog,
    time_picker_dialog,
    Context,
    EditText,
)


class TestParseDateTime:
    @pytest.mark.parametrize(
        "date_str, fmt",
        [
            ("15/07/2023", DateFormats.S_DDMMYYYY),
            ("2023-07-15", DateFormats.D_YYYYMMDD),
            ("15-Jul-2023", DateFormats.D_DDMMYYYY_N),
        ],
    )
    def test_parsing_valid_dates(self, date_str, fmt):
        assert parse_date(date_str, fmt) is not None

    @pytest.mark.parametrize(
        "date_str, fmt",
        [
            ("32/13/2023", DateFormats.D_DDMMYYYY),
            ("2023-02-30", DateFormats.D_YYYYMMDD),
            ("not-a-date", DateFormats.D_DDMMyy),
        ],
    )
    def test_parsing_invalid_dates(self, date_str, fmt):
        assert parse_date(date_str, fmt) is None

    @pytest.mark.parametrize(
        "date_str, fmt",
        [
            ("0001-01-01", DateFormats.D_YYYYMMDD),
            ("9999-12-31", DateFormats.D_YYYYMMDD),
            ("31-12-9999", DateFormats.D_DDMMYYYY),
        ],
    )
    def test_date_boundaries(self, date_str, fmt):
        assert parse_date(date_str, fmt) is not None

    @freeze_time("2023-07-15 14:30:45")
    def test_get_today_with_time(self):
        assert get_today_with_time() == "15/07/2023 14:30:45"

    @freeze_time("2023-07-15")
    def test_get_today(self):
        assert get_today() == "15/07/2023"

    @freeze_time("2023-07-15")
    def test_get_tomorrow(self):
        assert get_tomorrow() == "16/07/2023"

    @freeze_time("2023-12-31")
    def test_year_end(self):
        assert get_tomorrow() == "01/01/2024"

    @pytest.mark.parametrize(
        "timestamp,expected",
        [
            (1689415200000, "15/07/2023, 10:00AM"),  # 2023-07-15 14:00
            (1672531200000, "01/01/2023, 12:00AM"),  # New Year
        ],
    )
    def test_get_date_and_time(self, timestamp, expected):
        assert get_date_and_time(timestamp) == expected

    @pytest.mark.parametrize(
        "date_str,expected",
        [
            ("1689379200000", "15/07/2023, 12:00AM"),  # Valid timestamp
            ("invalid", "Invalid timestamp"),  # Invalid input
        ],
    )
    def test_get_date_and_time_str(self, date_str, expected):
        assert get_date_and_time_str(date_str) == expected

    @freeze_time("2023-07-15 04:30:45")
    @pytest.mark.parametrize(
        "days,expected",
        [
            (0, "15/07/2023"),
            (1, "16/07/2023"),
        ],
    )
    def test_get_date_only(self, days, expected):
        ts = int((datetime.now() + timedelta(days=days)).timestamp() * 1000)
        assert get_date_only(ts) == expected

    @pytest.mark.parametrize(
        "date_str,expected",
        [
            ("15/07/2023", 1689379200000),  # Valid
            ("invalid-date", None),  # Invalid
            ("29/02/2020", 1582934400000),  # Leap day
        ],
    )
    def test_get_date_only_str(self, date_str, expected):
        result = get_date_only_str(date_str)
        assert result == expected if expected else result is None

    @pytest.mark.parametrize(
        "hour,minute,expected",
        [
            (0, 0, "12:00AM"),  # Midnight
            (12, 0, "12:00PM"),  # Noon
            (23, 59, "11:59PM"),  # End of day
        ],
    )
    def test_get_time_only(self, hour, minute, expected):
        ts = int(
            datetime(2023, 7, 15, hour, minute, tzinfo=timezone.utc).timestamp() * 1000
        )
        assert get_time_only(ts) == expected

    @pytest.mark.parametrize(
        "date_str,expected",
        [
            ("15-Jul-23", 1437609600000),
            # TODO: Faulty as it could be 2015 or 2023
            ("2023/07/15", 1689379200000),
            ("invalid", None),
        ],
    )
    def test_parse_any_date(self, date_str, expected):
        result = parse_any_date(date_str)
        assert result == expected if expected else result is None

    @pytest.mark.parametrize(
        "fmt,expected_pattern",
        [
            (DateFormats.D_YYMMDD_N, r"\d{2}-\w{3}-\d{2}"),
            (DateFormats.S_YYYYMMDDHHMMA, r"\d{4}/\d{2}/\d{2}, \d{2}:\d{2}[AP]M"),
        ],
    )
    def test_get_desired_format(self, fmt, expected_pattern):
        result = get_desired_format(fmt)
        assert re.match(expected_pattern, result)

    @freeze_time("2023-07-15 04:30:45")
    @pytest.mark.parametrize(
        "timestamp,expected_pattern",
        [
            (
                int(
                    datetime(2023, 7, 15, 14, 30, tzinfo=timezone.utc).timestamp()
                    * 1000
                ),
                r"02:30 PM",
            ),
            # Today
            (
                int(
                    datetime(2023, 7, 14, 9, 15, tzinfo=timezone.utc).timestamp() * 1000
                ),
                r"14 Jul 09:15 AM",
            ),  # Yesterday
            (0, r"01 Jan 12:00 AM"),  # Epoch time
        ],
    )
    def test_prettify_date_str(self, timestamp, expected_pattern):
        assert re.search(expected_pattern, prettify_date_str(str(timestamp)))

    @freeze_time("2023-07-15 04:30:45")
    @pytest.mark.parametrize(
        "timestamp,expected",
        [
            (1689379200000, "12:00 AM"),  # 2023-07-15 14:00
            (0, "01 Jan 12:00 AM"),  # Epoch
            (1640995200000, "01 Jan 12:00 AM"),  # 2022-01-01
        ],
    )
    def test_prettify_date(self, timestamp, expected):
        assert prettify_date(timestamp) == expected

    @pytest.mark.parametrize(
        "date1,date2,fmt,expected",
        [
            (
                "15-07-2023, 02:00PM",
                "15-07-2023, 02:30PM",
                DateFormats.D_DDMMYYYYHHMMA,
                -30,
            ),
            (
                "01-07-2023, 12:00AM",
                "02-07-2023, 12:00AM",
                DateFormats.D_DDMMYYYYHHMMA,
                -1440,
            ),
            (
                "invalid-date",
                "02-07-2023, 12:00AM",
                DateFormats.D_DDMMYYYYHHMMA,
                None,
            ),
        ],
    )
    def test_get_minutes_between_two_dates(self, date1, date2, fmt, expected):
        assert get_minutes_between_two_dates(date1, date2, fmt) == expected

    @pytest.mark.parametrize(
        "days,expected",
        [
            (0, datetime.now().strftime("%d-%b-%y")),
            (7, (datetime.now() + timedelta(days=7)).strftime("%d-%b-%y")),
        ],
    )
    def test_get_date_from_days(self, days, expected):
        assert get_date_from_days(days) == expected

    @pytest.mark.parametrize(
        "date1,date2,fmt,expected",
        [
            # Valid same-day (UTC)
            ("15-07-2023", "15-07-2023", DateFormats.D_DDMMYYYY, 0),
            # Valid positive difference
            ("10-07-2023", "15-07-2023", DateFormats.D_DDMMYYYY, -5),
            # Valid negative difference
            ("20-07-2023", "15-07-2023", DateFormats.D_DDMMYYYY, 5),
            # Month boundary
            ("31-01-2023", "01-02-2023", DateFormats.D_DDMMYYYY, -1),
            # Leap year transition
            ("28-02-2020", "01-03-2020", DateFormats.D_DDMMYYYY, -2),
            # Invalid date
            ("invalid", "15-07-2023", DateFormats.D_DDMMYYYY, None),
        ],
    )
    def test_get_days_between_two_dates(self, date1, date2, fmt, expected):
        result = get_days_between_two_dates(date1, date2, fmt)
        assert result == expected

    @pytest.mark.parametrize(
        "date1,date2,fmt,expected",
        [
            # Same hour (UTC)
            (
                "15-07-2023, 2:00PM",
                "15-07-2023, 2:00PM",
                DateFormats.D_DDMMYYYYHHMMA,
                0,
            ),
            # Positive difference
            (
                "15-07-2023, 12:00PM",
                "15-07-2023, 2:00PM",
                DateFormats.D_DDMMYYYYHHMMA,
                -2,
            ),
            # Negative difference
            (
                "15-07-2023, 4:00PM",
                "15-07-2023, 2:00PM",
                DateFormats.D_DDMMYYYYHHMMA,
                2,
            ),
            # Midnight crossover
            (
                "31-12-2023, 11:00PM",
                "01-01-2024, 1:00AM",
                DateFormats.D_DDMMYYYYHHMMA,
                -2,
            ),
            # Invalid format
            (
                "15/07/2023, 2:00PM",
                "15-07-2023, 2:00PM",
                DateFormats.D_DDMMYYYYHHMMA,
                None,
            ),
        ],
    )
    def test_get_hours_between_two_dates(self, date1, date2, fmt, expected):
        result = get_hours_between_two_dates(date1, date2, fmt)
        assert result == expected

    # --------------------------
    # Boundary Cases
    # --------------------------
    @pytest.mark.parametrize(
        "date1,date2,fmt",
        [
            ("01-01-0001", "31-12-9999", DateFormats.D_DDMMYYYY),
            ("invalid-date", "invalid-date", DateFormats.D_DDMMYYYY),
        ],
    )
    def test_boundary_conditions(self, date1, date2, fmt):
        result = get_days_between_two_dates(date1, date2, fmt)
        assert result is None or isinstance(result, int)


class TestUIPicker:
    @freeze_time("2023-07-15 04:30:45")
    @pytest.mark.parametrize(
        "day, month, with_time, expected",
        [
            (31, 1, False, "31-01-2023"),  # January
            (28, 2, False, "28-02-2023"),  # Non-leap year
            (30, 4, True, "30-04-2023, 04:30 AM"),  # April
        ],
    )
    def test_date_selection(self, day, month, with_time, expected):
        edit_text = EditText()
        dialog = date_picker_dialog(
            Context(), edit_text, with_time, DateFormats.D_DDMMYYYY
        )
        dialog.on_date_set_listener(2023, month, day)
        assert edit_text.get_text() == expected

    @pytest.mark.parametrize(
        "hour,minute,expected",
        [(14, 30, "02:30 PM"), (23, 59, "11:59 PM"), (0, 0, "12:00 AM")],
    )
    def test_time_selection(self, hour, minute, expected):
        edit_text = EditText()
        dialog = time_picker_dialog(
            context=Context(), date_edit_text=edit_text, with_append=False
        )
        dialog.on_time_set_listener(hour, minute)
        assert edit_text.get_text() == expected
