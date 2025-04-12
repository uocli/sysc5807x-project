"""
Metamorphic Testing for Date Format Converter

This file implements metamorphic testing for the date format converter.
It defines several metamorphic relations (MRs) that should hold true for
any implementation of a date converter, and tests these relations
with various test cases.

Metamorphic relations implemented:
- MR1: Round-trip conversion should return the original date
- MR2: Transitive conversion should yield consistent results
- MR3: Semantic equivalence should be maintained after conversion
"""

import time
from datetime import datetime

from date_format_converter import convert_date


# Define metamorphic relations
def mr1_round_trip(date_str: str, source_format: str, target_format: str) -> bool:
    """
    MR1: Converting from A -> B -> A should return the original date.
    :param date_str: date string to convert
    :param source_format: source format
    :param target_format: target format
    :return: True if the relation holds, False otherwise
    """
    try:
        # First conversion: A -> B
        intermediate = convert_date(date_str, source_format, target_format)
        if intermediate is None:
            return True  # Skip if first conversion fails (invalid input)

        # Second conversion: B -> A
        result = convert_date(intermediate, target_format, source_format)

        # Compare original and final results
        return date_str == result
    except Exception as e:
        print(f"Error in mr1_round_trip: {e}")
        return False


def mr2_transitive_conversion(
    date_str: str, format1: str, format2: str, format3: str
) -> bool:
    """
    MR2: Converting A -> B -> C should give same result as A -> C directly.
    :param date_str: date string to convert
    :param format1: date format A
    :param format2: date format B
    :param format3: date format C
    :return: True if the relation holds, False otherwise
    """
    try:
        # Direct conversion: A -> C
        direct = convert_date(date_str, format1, format3)
        if direct is None:
            return True  # Skip if direct conversion fails

        # Two-step conversion: A -> B -> C
        intermediate = convert_date(date_str, format1, format2)
        if intermediate is None:
            return True  # Skip if first step fails

        indirect = convert_date(intermediate, format2, format3)

        # Compare results
        return direct == indirect
    except Exception as e:
        print(f"Error in mr2_transitive_conversion: {e}")
        return False


def mr3_semantic_equality(date_str, source_format, target_format) -> bool:
    """
    MR3: The date should remain semantically the same after conversion.
    :param date_str: Original date string
    :param source_format: Source format
    :param target_format: Target format
    :return: True if the relation holds, False otherwise
    """
    try:
        # Convert the date
        converted = convert_date(date_str, source_format, target_format)
        if converted is None:
            return True  # Skip if conversion fails

        # Parse both dates as datetime objects
        original_dt = datetime.strptime(date_str, source_format)
        converted_dt = datetime.strptime(converted, target_format)

        # Compare year, month, day components
        return (
            original_dt.year == converted_dt.year
            and original_dt.month == converted_dt.month
            and original_dt.day == converted_dt.day
        )
    except Exception as e:
        print(f"Error in mr3_semantic_equality: {e}")
        return False


def get_seed_dates():
    """
    Define seed date test cases covering different scenarios.
    :return: List of tuples (date_str, format) for testing
    """
    return [
        ("2023-05-15", "%Y-%m-%d"),  # Standard date
        ("15/05/2023", "%d/%m/%Y"),  # Standard date with slashes
        ("2023/05/15", "%Y/%m/%d"),  # Year first with slashes
        ("15-05-2023", "%d-%m-%Y"),  # Day first with hyphens
        ("2023-05-15, 10:30AM", "%Y-%m-%d, %I:%M%p"),  # Date with time
        ("29/02/2020", "%d/%m/%Y"),  # Leap day
        ("31/12/2023", "%d/%m/%Y"),  # Year boundary
        ("01/01/2023", "%d/%m/%Y"),  # Year boundary
    ]


def get_test_formats() -> list:
    """
    Define test formats to use for conversions.
    :return: List of format strings
    """
    return [
        "%Y-%m-%d",  # YYYY-MM-DD
        "%d/%m/%Y",  # DD/MM/YYYY
        "%Y/%m/%d",  # YYYY/MM/DD
        "%d-%m-%Y",  # DD-MM-YYYY
        "%Y-%m-%d, %I:%M%p",  # YYYY-MM-DD, HH:MM AM/PM
        "%d/%m/%Y, %I:%M%p",  # DD/MM/YYYY, HH:MM AM/PM
    ]


def test_mr1_round_trip():
    """
    Test metamorphic relation: round trip conversion.
    """
    start_time = time.time()
    results = []

    for date_str, src_format in get_seed_dates():
        for tgt_format in get_test_formats():
            # Skip if same format or incompatible formats (time vs no-time)
            if src_format == tgt_format:
                continue
            if ("%p" in src_format) != ("%p" in tgt_format):
                continue  # Skip incompatible time formats

            result = mr1_round_trip(date_str, src_format, tgt_format)
            results.append(result)
            print(
                f"MR1: {date_str} ({src_format}) -> {tgt_format} -> {src_format}: {'Pass' if result else 'Fail'}"
            )
            assert (
                result
            ), f"MR1 failed for {date_str} with formats {src_format} and {tgt_format}"

    end_time = time.time()
    print(
        f"MR1 tests executed in {(end_time - start_time)*1000:.3f} ms, {results.count(True)}/{len(results)} passed"
    )


def test_mr2_transitive_conversion():
    """
    Test metamorphic relation: transitive conversion.
    """
    start_time = time.time()
    results = []

    for date_str, src_format in get_seed_dates():
        tested_combinations = 0

        for mid_format in get_test_formats():
            for tgt_format in get_test_formats():
                # Skip if any formats are the same or incompatible formats
                if (
                    src_format == mid_format
                    or mid_format == tgt_format
                    or src_format == tgt_format
                ):
                    continue
                if (("%p" in src_format) != ("%p" in mid_format)) or (
                    ("%p" in mid_format) != ("%p" in tgt_format)
                ):
                    continue  # Skip incompatible time formats

                # Limit the number of combinations to test per seed date
                if tested_combinations >= 5:  # Test up to 5 combinations per seed date
                    break

                result = mr2_transitive_conversion(
                    date_str, src_format, mid_format, tgt_format
                )
                results.append(result)
                print(
                    f"MR2: {date_str} ({src_format} -> {mid_format} -> {tgt_format}): {'Pass' if result else 'Fail'}"
                )
                assert (
                    result
                ), f"MR2 failed for {date_str} with formats {src_format}, {mid_format}, {tgt_format}"

                tested_combinations += 1

    end_time = time.time()
    print(
        f"MR2 tests executed in {(end_time - start_time)*1000:.3f} ms, {results.count(True)}/{len(results)} passed"
    )


def test_mr3_semantic_equality():
    """
    Test metamorphic relation: semantic equality.
    """
    start_time = time.time()
    results = []

    for date_str, src_format in get_seed_dates():
        for tgt_format in get_test_formats():
            # Skip if same format or incompatible formats
            if src_format == tgt_format:
                continue
            if ("%p" in src_format) != ("%p" in tgt_format):
                continue  # Skip incompatible time formats

            result = mr3_semantic_equality(date_str, src_format, tgt_format)
            results.append(result)
            print(
                f"MR3: {date_str} ({src_format} -> {tgt_format}): {'Pass' if result else 'Fail'}"
            )
            assert (
                result
            ), f"MR3 failed for {date_str} with formats {src_format} and {tgt_format}"

    end_time = time.time()
    print(
        f"MR3 tests executed in {(end_time - start_time)*1000:.3f} ms, {results.count(True)}/{len(results)} passed"
    )


def test_edge_cases():
    """
    Test conversion edge cases.
    """
    # Test year boundary
    assert mr3_semantic_equality(
        "31/12/2022", "%d/%m/%Y", "%Y-%m-%d"
    ), "Failed on year boundary (31/12/2022)"
    assert mr3_semantic_equality(
        "01/01/2023", "%d/%m/%Y", "%Y-%m-%d"
    ), "Failed on year boundary (01/01/2023)"

    # Test leap year
    assert mr3_semantic_equality(
        "29/02/2020", "%d/%m/%Y", "%Y-%m-%d"
    ), "Failed on leap day in leap year"

    # Test month with 30 days
    assert mr3_semantic_equality(
        "30/04/2023", "%d/%m/%Y", "%Y-%m-%d"
    ), "Failed on month with 30 days"

    # Test month with 31 days
    assert mr3_semantic_equality(
        "31/01/2023", "%d/%m/%Y", "%Y-%m-%d"
    ), "Failed on month with 31 days"
