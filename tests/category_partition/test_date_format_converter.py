import time
from datetime import datetime
from typing import Optional

from date_format_converter import convert_date, DateFormats


def generate_date_inputs() -> dict:
    return {
        # Valid Dates
        "valid_dates": [
            # Leap year (valid)
            ("2020-02-29", DateFormats.D_YYYYMMDD),
            # Month boundaries
            ("2023-04-30", DateFormats.D_YYYYMMDD),
            ("30-04-2023", DateFormats.D_DDMMYYYY),
            # Separate case for DD-MM-YYYY
            # Year boundaries
            ("0001-01-01", DateFormats.D_YYYYMMDD),
            ("31-12-9999", DateFormats.D_DDMMYYYY),
        ],
        # Invalid Dates
        "invalid_dates": [
            # Invalid day
            ("2023-02-30", DateFormats.D_YYYYMMDD),
            # Invalid month
            ("2023-13-01", DateFormats.D_YYYYMMDD),
            # Wrong separator
            ("2023/05-15", DateFormats.D_YYYYMMDD),
        ],
        # Time Components
        "time_dates": [
            # Midnight/noon edge cases
            ("2023-05-15, 12:00AM", DateFormats.D_YYYYMMDDHHMMA),
            ("15-05-2023, 12:00PM", DateFormats.D_DDMMYYYYHHMMA),
            # With seconds
            ("2023-05-15, 11:59:59PM", DateFormats.D_YYYYMMDDHHMMSSA),
        ],
        # Edge Scenarios
        "edge_dates": [
            # Epoch time
            ("1970-01-01", DateFormats.D_YYYYMMDD),
            # Near-future date
            (datetime.now().strftime("%Y-%m-%d"), DateFormats.D_YYYYMMDD),
        ],
        # Error Handling
        "error_cases": [
            # Non-date strings
            ("not-a-date", DateFormats.D_YYYYMMDD),
            # Empty input
            ("", DateFormats.D_YYYYMMDD),
        ],
    }


def is_valid_date(date_str, format_enum) -> bool:
    """
    Check if a date string is valid according to its format
    :param date_str: string representation of the date
    :param format_enum: Enum representing the date format
    :return: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, format_enum.get_date_format())
        return True
    except ValueError:
        return False


def is_compatible_format(source_format, target_format) -> bool:
    """
    Check if the source and target formats are compatible for conversion
    :param source_format: Source date format
    :param target_format: Target date format
    :return: True if compatible, False otherwise
    """
    # Check if both formats have time or both do not have time
    return ("HH" in source_format.value) == ("HH" in target_format.value)


def execute_conversion(date_str, source_format, target_format) -> Optional[str]:
    """
    Execute the date conversion and measure the time taken
    :param date_str: string representation of the date
    :param source_format: source date format
    :param target_format: target date format
    :return: a tuple containing the result and the time taken in milliseconds
    """
    start_time = time.time()
    result = convert_date(date_str, source_format.value, target_format.value)
    end_time = time.time()
    print(
        f"Converting {date_str} from {source_format.name} to {target_format.name}: {result} ({(end_time - start_time) * 1000:.3f} ms)"
    )
    return result


def test_valid_date_conversion():
    date_inputs = generate_date_inputs()
    for date_str, source_format in date_inputs["valid_dates"]:
        for target_format in DateFormats:
            if not is_compatible_format(source_format, target_format):
                continue  # Skip incompatible formats

            result = convert_date(date_str, source_format.value, target_format.value)
            assert result is not None, f"Failed: {date_str} → {target_format.name}"
            assert is_valid_date(result, target_format), f"Invalid output: {result}"


def test_edge_case_conversion():
    date_inputs = generate_date_inputs()
    for date_str, source_format in date_inputs["edge_dates"]:
        for target_format in DateFormats:
            result = convert_date(date_str, source_format.value, target_format.value)
            assert result is not None, f"Edge case failed: {date_str}"
            assert is_valid_date(
                result, target_format
            ), f"Invalid edge result: {result}"


def test_invalid_date_conversion():
    date_inputs = generate_date_inputs()
    for date_str, source_format in (
        date_inputs["invalid_dates"] + date_inputs["error_cases"]
    ):
        for target_format in DateFormats:
            result = convert_date(date_str, source_format.value, target_format.value)
            assert (
                result is None
            ), f"Unexpected success: {date_str} → {target_format.name}"


def test_time_conversion():
    date_inputs = generate_date_inputs()
    for date_str, source_format in date_inputs["time_dates"]:
        for target_format in DateFormats:
            if "HH" not in target_format.value:
                continue  # Skip date-only formats

            result = convert_date(date_str, source_format.value, target_format.value)
            assert result is not None, f"Time conversion failed: {date_str}"
            assert "12:00" in result or "23:59" in result, "Time component corrupted"


def test_boundary_conditions():
    # Test epoch time conversion
    epoch_result = convert_date("1970-01-01", "%Y-%m-%d", "%d/%m/%Y")
    assert epoch_result == "01/01/1970", "Epoch time conversion failed"

    # Test near-future date (today)
    today = datetime.now().strftime("%Y-%m-%d")
    today_result = convert_date(today, "%Y-%m-%d", "%d-%b-%Y")
    assert datetime.strptime(today_result, "%d-%b-%Y"), "Today conversion failed"
