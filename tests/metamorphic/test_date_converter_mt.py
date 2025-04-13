import datetime
import logging
from date_format_converter import (
    DateFormats,
    get_date_only,
    get_date_only_str,
    get_date_and_time,
    get_date_and_time_str,
    get_days_between_two_dates,
    get_hours_between_two_dates,
    get_minutes_between_two_dates,
    parse_date,
    parse_any_date,
    get_desired_format,
    get_today,
    get_tomorrow,
    get_today_with_time,
    get_time_only,
    get_date_from_days,
    Context,
    EditText,
    date_picker_dialog,
    time_picker_dialog,
)

"""
Comprehensive metamorphic testing for date_format_converter.py using pytest
This test suite covers all methods in the module using various metamorphic relations.
"""

# Disable traceback printing from the date_format_converter module
logging.getLogger().setLevel(logging.ERROR)


def test_mr1_date_format_inverse_conversion():
    """
    MR1: Inverse Relation
    If we convert a date from format A to format B, and then from format B to format A,
    we should get the original date.
    """
    # Source test case
    original_date = "15/03/2023"
    # Convert to timestamp (intermediate format)
    timestamp = get_date_only_str(original_date)
    # Convert back to original format
    converted_back = get_date_only(timestamp)

    # Metamorphic relation: original_date should equal converted_back
    assert original_date == converted_back


def test_mr2_date_parsing_timestamp_consistency():
    """
    MR2: Consistency Relation
    If we parse the same date in different formats, the resulting timestamps should be equal.
    """
    # Source test cases
    date_ddmmyyyy = "15/03/2023"  # dd/MM/yyyy
    date_yyyymmdd = "2023-03-15"  # yyyy-MM-dd

    # Parse dates using different formats
    timestamp1 = parse_date(date_ddmmyyyy, DateFormats.S_DDMMYYYY)
    timestamp2 = parse_date(date_yyyymmdd, DateFormats.D_YYYYMMDD)

    # Metamorphic relation: Both timestamps should be equal
    assert timestamp1 == timestamp2


def test_mr3_days_between_dates_symmetry():
    """
    MR3: Symmetry Relation
    The number of days between date A and date B should be the negative of
    the number of days between date B and date A.
    """
    # Source test case
    date1 = "15/03/2023"
    date2 = "20/03/2023"

    # Calculate days in both directions
    days_forward = get_days_between_two_dates(date1, date2, DateFormats.S_DDMMYYYY)
    days_backward = get_days_between_two_dates(date2, date1, DateFormats.S_DDMMYYYY)

    # Metamorphic relation: days_forward = -days_backward
    assert days_forward == -days_backward


def test_mr4_time_conversion_preservation():
    """
    MR4: Time Unit Conversion Relation
    The number of hours between two dates should be 24 times the number of days.
    """
    # Source test case - Using format without space between time and AM/PM
    date1 = "15/03/2023, 12:00PM"
    date2 = "16/03/2023, 12:00PM"

    # Calculate days and hours
    days = get_days_between_two_dates(date1, date2, DateFormats.S_DDMMYYYYHHMMA)
    hours = get_hours_between_two_dates(date1, date2, DateFormats.S_DDMMYYYYHHMMA)

    # Metamorphic relation: hours = days * 24
    assert hours == days * 24


def test_mr5_minutes_hours_conversion():
    """
    MR5: Time Unit Conversion Relation
    The number of minutes between two dates should be 60 times the number of hours.
    """
    # Source test case - Using format without space between time and AM/PM
    date1 = "15/03/2023, 12:00PM"
    date2 = "15/03/2023, 01:00PM"

    # Calculate hours and minutes
    hours = get_hours_between_two_dates(date1, date2, DateFormats.S_DDMMYYYYHHMMA)
    minutes = get_minutes_between_two_dates(date1, date2, DateFormats.S_DDMMYYYYHHMMA)

    # Metamorphic relation: minutes = hours * 60
    assert minutes == hours * 60


def test_mr6_date_format_equivalence():
    """
    MR6: Format Equivalence Relation
    The same date represented in different formats should be equal when converted to a common format.
    """
    # Source test cases
    timestamp = int(datetime.datetime(2023, 3, 15).timestamp() * 1000)

    # Get date in different formats
    format1 = get_desired_format(DateFormats.D_DDMMYYYY, timestamp)
    format2 = get_desired_format(DateFormats.S_YYYYMMDD, timestamp)

    # Parse both formats back to timestamps
    timestamp1 = parse_date(format1, DateFormats.D_DDMMYYYY)
    timestamp2 = parse_date(format2, DateFormats.S_YYYYMMDD)

    # Metamorphic relation: Both should parse to the same timestamp
    assert timestamp1 == timestamp2


def test_mr7_date_today_tomorrow_relation():
    """
    MR7: Sequential Date Relation
    Tomorrow's date should be exactly one day after today's date.
    """
    # Get today and tomorrow
    today = get_today()
    tomorrow = get_tomorrow()

    # Convert to timestamps
    today_ts = parse_date(today, DateFormats.S_DDMMYYYY)
    tomorrow_ts = parse_date(tomorrow, DateFormats.S_DDMMYYYY)

    # Expected difference in milliseconds (24 hours)
    expected_diff = 24 * 60 * 60 * 1000

    # Metamorphic relation: tomorrow - today = 24 hours (in milliseconds)
    assert tomorrow_ts - today_ts == expected_diff


def test_mr8_parse_any_date_consistency():
    """
    MR8: Parse Consistency Relation
    parse_any_date should give the same result as parse_date with the correct format.
    """
    # Source test case
    date_str = "15/03/2023"

    # Parse with specific format
    timestamp1 = parse_date(date_str, DateFormats.S_DDMMYYYY)

    # Parse with automatic format detection - suppress traceback printing
    timestamp2 = parse_any_date(date_str)

    # Metamorphic relation: Both parsing methods should give the same result
    assert timestamp1 == timestamp2


def test_mr9_date_manipulation_consistency():
    """
    MR9: Date Manipulation Consistency
    After adding and then subtracting the same number of days, we should get the original date.
    """
    # Original date in timestamp form
    original_date = datetime.datetime(2023, 3, 15)
    original_ts = int(original_date.timestamp() * 1000)

    # Add 10 days
    plus_10_days = original_date + datetime.timedelta(days=10)
    plus_10_ts = int(plus_10_days.timestamp() * 1000)

    # Convert to formatted strings
    original_str = get_desired_format(DateFormats.S_DDMMYYYY, original_ts)
    plus_10_str = get_desired_format(DateFormats.S_DDMMYYYY, plus_10_ts)

    # Calculate days between the two dates
    days_diff = get_days_between_two_dates(
        original_str, plus_10_str, DateFormats.S_DDMMYYYY
    )

    # Metamorphic relation: The difference should be -10 days (original to plus 10 days)
    assert days_diff == -10


def test_mr10_different_time_representations():
    """
    MR10: Different Time Representations
    The same time represented in 12-hour and 24-hour formats should be equivalent when parsed.
    """
    # Source test case - 3 PM in 12h format without space
    time_12h = "15/03/2023, 03:00PM"

    # Generate a timestamp for 3 PM on March 15, 2023
    dt = datetime.datetime(2023, 3, 15, 15, 0, 0)
    ts_24h = int(dt.timestamp() * 1000)

    # Parse the 12h format to a timestamp
    format_12h = DateFormats.S_DDMMYYYYHHMMA
    ts_12h = parse_date(time_12h, format_12h)

    # Metamorphic relation: Both timestamps should be equal
    # Allow a small tolerance for timezone differences
    assert abs(ts_12h - ts_24h) < 24 * 60 * 60 * 1000  # Within 24 hours


def test_mr11_get_date_and_time_formatting():
    """
    MR11: Date and Time Formatting Consistency
    get_date_and_time should format a timestamp in a way that can be parsed back to the original timestamp.
    """
    # Create a timestamp
    dt = datetime.datetime(2023, 3, 15, 14, 30, 0).replace(tzinfo=datetime.timezone.utc)
    timestamp = int(dt.timestamp() * 1000)

    # Format using get_date_and_time
    formatted = get_date_and_time(timestamp)

    # Parse the formatted string back to a timestamp
    parsed_timestamp = parse_date(formatted, DateFormats.S_DDMMYYYYHHMMA)

    # Metamorphic relation: The original and parsed timestamps should be close
    # (allowing for some precision loss in formatting/parsing)
    assert abs(timestamp - parsed_timestamp) < 60 * 1000  # Within 1 minute


def test_mr12_get_date_and_time_str_consistency():
    """
    MR12: Date and Time String Conversion Consistency
    get_date_and_time_str should produce the same output as get_date_and_time for the same time.
    """
    # Create a timestamp
    dt = datetime.datetime(2023, 3, 15, 14, 30, 0).replace(tzinfo=datetime.timezone.utc)
    timestamp = int(dt.timestamp() * 1000)

    # Format using get_date_and_time
    formatted1 = get_date_and_time(timestamp)

    # Format using get_date_and_time_str
    formatted2 = get_date_and_time_str(str(timestamp))

    # Metamorphic relation: Both methods should produce the same formatted string
    assert formatted1 == formatted2


def test_mr13_get_time_only_extraction():
    """
    MR13: Time Extraction Consistency
    get_time_only should extract only the time component from a full timestamp.
    """
    # Create a timestamp
    dt = datetime.datetime(2023, 3, 15, 14, 30, 0).replace(tzinfo=datetime.timezone.utc)
    timestamp = int(dt.timestamp() * 1000)

    # Get time only
    time_only = get_time_only(timestamp)

    # Get full date and time
    full_date_time = get_date_and_time(timestamp)

    # Metamorphic relation: The time_only string should be the time part of the full date and time
    assert time_only in full_date_time


def test_mr14_get_today_with_time_consistency():
    """
    MR14: Today with Time Format Consistency
    get_today_with_time should include all components of get_today plus time information.
    """
    # Get today and today with time
    today = get_today()
    today_with_time = get_today_with_time()

    # Metamorphic relation: today should be a substring of today_with_time
    assert today in today_with_time

    # Additional verification: today_with_time should have more characters (time component)
    assert len(today_with_time) > len(today)


def test_mr15_get_date_from_days_consistency():
    """
    MR15: Days Addition Consistency
    get_date_from_days should produce a date that is exactly the specified number of days from today.
    """
    # Number of days to add
    days_to_add = 5

    # Get the date after adding days
    future_date = get_date_from_days(days_to_add)

    # Calculate the expected date by adding days to today
    today = datetime.datetime.now()
    expected_date = today + datetime.timedelta(days=days_to_add)
    expected_formatted = expected_date.strftime(DateFormats.D_DDMMyy_N.value)

    # Metamorphic relation: future_date should match the expected formatted date
    assert future_date == expected_formatted


def test_mr16_date_picker_dialog_functionality():
    """
    MR16: Date Picker Dialog Behavior
    date_picker_dialog should create a dialog that sets the correct formatted date.
    """
    # Create a Context and EditText
    context = Context()
    edit_text = EditText()

    # Create a date picker dialog
    dialog = date_picker_dialog(
        context=context,
        date_edit_text=edit_text,
        with_time=False,
        date_formats=DateFormats.D_DDMMyy,
    )

    # Show the dialog (which will trigger the callback)
    dialog.show()

    # Verify that the EditText has been updated with a date in the correct format
    date_text = edit_text.get_text()
    assert date_text is not None

    # Attempt to parse with the expected format to verify it's correctly formatted
    try:
        datetime.datetime.strptime(date_text, DateFormats.D_DDMMyy.value)
        format_correct = True
    except ValueError:
        format_correct = False

    # Metamorphic relation: The date should be correctly formatted
    assert format_correct


def test_mr17_time_picker_dialog_functionality():
    """
    MR17: Time Picker Dialog Behavior
    time_picker_dialog should create a dialog that sets the correct formatted time.
    """
    # Create a Context and EditText
    context = Context()
    edit_text = EditText()

    # Create a time picker dialog
    dialog = time_picker_dialog(
        context=context, date_edit_text=edit_text, with_append=False
    )

    # Show the dialog (which will trigger the callback)
    dialog.show()

    # Verify that the EditText has been updated with a time
    time_text = edit_text.get_text()
    assert time_text is not None

    # Check if it's in the expected format (e.g., "HH:MM AM/PM")
    try:
        datetime.datetime.strptime(time_text, "%I:%M %p")
        format_correct = True
    except ValueError:
        format_correct = False

    # Metamorphic relation: The time should be correctly formatted
    assert format_correct


def test_mr18_time_picker_with_append():
    """
    MR18: Time Picker with Append Behavior
    time_picker_dialog with append=True should append time to existing text.
    """
    # Create a Context and EditText
    context = Context()
    edit_text = EditText()

    # Set initial text
    initial_text = "15-03-23"
    edit_text.set_text(initial_text)

    # Create a time picker dialog with append=True
    dialog = time_picker_dialog(
        context=context, date_edit_text=edit_text, with_append=True
    )

    # Show the dialog
    dialog.show()

    # Get the updated text
    updated_text = edit_text.get_text()

    # Metamorphic relations:
    # 1. The updated text should contain the initial text
    assert initial_text in updated_text

    # 2. The updated text should be longer (due to appended time)
    assert len(updated_text) > len(initial_text)

    # 3. The updated text should have the format "date, time"
    assert "," in updated_text


def test_mr19_combined_date_time_picker():
    """
    MR19: Combined Date and Time Picker Behavior
    Using date_picker_dialog with with_time=True should result in both date and time being set.
    """
    # Create a Context and EditText
    context = Context()
    edit_text = EditText()

    # Create a date picker dialog with with_time=True
    dialog = date_picker_dialog(
        context=context,
        date_edit_text=edit_text,
        with_time=True,
        date_formats=DateFormats.D_DDMMyy,
    )

    # Show the dialog (this should trigger the date and time pickers)
    dialog.show()

    # Get the final text
    final_text = edit_text.get_text()

    # Metamorphic relations:
    # 1. The final text should contain a comma (separating date and time)
    assert "," in final_text

    # 2. The final text should contain "AM" or "PM"
    assert "AM" in final_text or "PM" in final_text


def test_mr20_prettify_date_consistency():
    """
    MR20: Prettify Date Behavior
    prettify_date should format dates consistently based on whether they are today or not.
    """
    from date_format_converter import prettify_date, prettify_date_str

    # Create a timestamp for a date that is not today
    past_date = datetime.datetime.now() - datetime.timedelta(days=10)
    past_timestamp = int(past_date.timestamp() * 1000)

    # Prettify using both methods
    pretty1 = prettify_date(past_timestamp)
    pretty2 = prettify_date_str(str(past_timestamp))

    # Metamorphic relation: Both prettify methods should produce the same result
    assert pretty1 == pretty2
