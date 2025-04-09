from src.date_format_converter import DateFormats


def generate_date_inputs() -> dict:
    """
    Generate various date inputs for testing
    :return: A dictionary containing lists of date strings and their formats
    """
    # Regular dates (known valid dates in various formats)
    regular_dates = [
        # Format: (date_string, format)
        ("2023-05-15", DateFormats.D_YYYYMMDD),
        ("15-05-2023", DateFormats.D_DDMMYYYY),
        ("2023/05/15", DateFormats.S_YYYYMMDD),
        ("15/05/2023", DateFormats.S_DDMMYYYY),
        ("23-05-15", DateFormats.D_YYMMDD),
        ("15-05-23", DateFormats.D_DDMMyy),
        ("23/05/15", DateFormats.S_YYMMDD),
        ("15/05/23", DateFormats.S_DDMMyy),
    ]

    # Edge case dates
    edge_dates = [
        # Format: (date_string, format)
        # Leap year day
        ("2020-02-29", DateFormats.D_YYYYMMDD),
        ("29-02-2020", DateFormats.D_DDMMYYYY),
        # Month boundaries
        ("2023-01-31", DateFormats.D_YYYYMMDD),
        ("30-04-2023", DateFormats.D_DDMMYYYY),
        # Year boundaries
        ("2000-01-01", DateFormats.D_YYYYMMDD),
        ("31-12-1999", DateFormats.D_DDMMYYYY),
    ]

    # Invalid dates
    invalid_dates = [
        # Format: (date_string, format)
        # Day out of range
        ("2023-02-30", DateFormats.D_YYYYMMDD),
        ("31-04-2023", DateFormats.D_DDMMYYYY),
        # Month out of range
        ("2023-13-01", DateFormats.D_YYYYMMDD),
        ("01-13-2023", DateFormats.D_DDMMYYYY),
        # Non-leap year Feb 29
        ("2023-02-29", DateFormats.D_YYYYMMDD),
        # Invalid characters
        ("2023-O5-15", DateFormats.D_YYYYMMDD),
        # Wrong separator
        ("2023/05-15", DateFormats.D_YYYYMMDD),
    ]

    # Dates with time
    dates_with_time = [
        # Format: (date_string, format)
        ("2023-05-15, 10:30AM", DateFormats.D_YYYYMMDDHHMMA),
        ("15-05-2023, 10:30AM", DateFormats.D_DDMMYYYYHHMMA),
        ("2023/05/15, 10:30AM", DateFormats.S_YYYYMMDDHHMMA),
        ("15/05/2023, 10:30AM", DateFormats.S_DDMMYYYYHHMMA),
    ]

    return {
        "regular_dates": regular_dates,
        "edge_dates": edge_dates,
        "invalid_dates": invalid_dates,
        "dates_with_time": dates_with_time,
    }


def generate_format_combinations() -> list:
    """
    Generate combinations of source and target formats for conversion
    :return: A list of tuples containing source and target formats
    """
    # Select a subset of formats to test
    formats = [
        DateFormats.D_YYYYMMDD,  # YYYY-MM-DD
        DateFormats.D_DDMMYYYY,  # DD-MM-YYYY
        DateFormats.S_YYYYMMDD,  # YYYY/MM/DD
        DateFormats.S_DDMMYYYY,  # DD/MM/YYYY
        DateFormats.D_YYMMDD,  # YY-MM-DD
        DateFormats.D_DDMMyy,  # DD-MM-YY
    ]

    # Generate all combinations of formats
    combinations = []
    for src_format in formats:
        for tgt_format in formats:
            if src_format != tgt_format:
                combinations.append((src_format, tgt_format))

    return combinations
