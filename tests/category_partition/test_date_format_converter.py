import time
from datetime import datetime
from typing import Optional

from src.date_format_converter import convert_date, DateFormats
from date_format_converter_categories import generate_date_inputs


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


def test_date_conversion_regular():
    """
    Test converting regular valid dates between formats
    """
    date_inputs = generate_date_inputs()

    for date_str, source_format in date_inputs["regular_dates"]:
        for target_format in [fmt for fmt in DateFormats if fmt != source_format]:
            # Skip incompatible format combinations (e.g., date-only to date-time)
            if is_compatible_format(source_format, target_format):
                continue

            result = execute_conversion(date_str, source_format, target_format)

            # Verify result is not None for valid dates
            assert (
                result is not None
            ), f"Conversion failed for {date_str} from {source_format.name} to {target_format.name}"

            # Verify the result date is valid according to target format
            assert is_valid_date(
                result, target_format
            ), f"Converted date {result} is not valid in format {target_format.name}"


def test_date_conversion_edge_cases():
    """
    Test converting edge cases between formats
    """
    date_inputs = generate_date_inputs()

    for date_str, source_format in date_inputs["edge_dates"]:
        for target_format in [fmt for fmt in DateFormats if fmt != source_format]:
            # Skip incompatible format combinations
            if is_compatible_format(source_format, target_format):
                continue

            result = execute_conversion(date_str, source_format, target_format)

            # For valid edge cases, verify the result
            if is_valid_date(date_str, source_format):
                assert result is not None
                assert is_valid_date(result, target_format)


def test_date_conversion_invalid():
    """Test behavior when converting invalid dates"""
    date_inputs = generate_date_inputs()

    for date_str, source_format in date_inputs["invalid_dates"]:
        for target_format in [fmt for fmt in DateFormats if fmt != source_format]:
            # Skip incompatible format combinations
            if is_compatible_format(source_format, target_format):
                continue

            result = execute_conversion(date_str, source_format, target_format)

            # The function should either return None or handle the error appropriately
            # Adjust this assertion based on how your convert_date function handles invalid inputs
            assert result is None or "Invalid" in str(result)
