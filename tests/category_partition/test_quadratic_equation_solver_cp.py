import pytest
import builtins


def generate_automated_test_cases():
    """
    Automatically generate test cases using category-partition method.
    Return a list of (inputs, expected_outputs) tuples.
    """
    test_cases = []

    # Define categories for discriminant
    discriminant_categories = [
        ("positive", lambda a, b, c: b**2 - 4 * a * c > 0),  # Two real roots
        ("zero", lambda a, b, c: abs(b**2 - 4 * a * c) < 1e-10),  # One repeated root
        ("negative", lambda a, b, c: b**2 - 4 * a * c < 0),  # Complex roots
    ]

    # Define test values for each coefficient
    a_values = [0.0001, -0.0001, 1, -1, 100, -100, 10000, -10000]
    b_values = [0, 0.0001, -0.0001, 1, -1, 100, -100, 10000, -10000]
    c_values = [0, 0.0001, -0.0001, 1, -1, 100, -100, 10000, -10000]

    # Generate test cases for each discriminant category
    for name, condition in discriminant_categories:
        # Try different coefficient combinations
        expected = []
        for a in a_values:
            for b in b_values:
                for c in c_values:
                    # Check if this combination satisfies the discriminant condition
                    if condition(a, b, c):
                        # Add the test case
                        inputs = [str(a), str(b), str(c), "n"]

                        if name in ["positive", "zero"]:
                            expected = ["Thank you"]
                        elif name == "negative":
                            expected = ["j"]  # Complex roots should have 'j' in output

                        test_cases.append((inputs, expected))

                        # Limit number of test cases per category to prevent explosion
                        if len([tc for tc in test_cases if tc[1] == expected]) >= 5:
                            break
                if len([tc for tc in test_cases if tc[1] == expected]) >= 5:
                    break
            if len([tc for tc in test_cases if tc[1] == expected]) >= 5:
                break

    # Add special case tests
    special_cases = [
        # a = 0 (rejection)
        (["0", "1", "-3", "2", "n"], ["'a' cannot be zero", "x1 = 2"]),
        # Non-numeric input
        (["abc", "1", "-3", "2", "n"], ["not allowed", "x1 = 2"]),
        # Multiple equations
        (
            ["1", "-3", "2", "y", "1", "0", "1", "n"],
            ["x1 = 2", "x2 = 1", "j"],
        ),
        # Too large or too small values
        (
            ["1.0e20", "-1.0e20", "1", "-3", "2", "n"],
            ["x1 = 2", "x2 = 1", "too large"],
        ),
        # nan
        (
            ["nan", "-3", "2", "n"],
            ["Failed to find an accurate solution"],
        ),
    ]

    test_cases.extend(special_cases)

    return test_cases


def simulate_inputs(monkeypatch, inputs):
    """Simulate user inputs for testing."""
    iterator = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _: next(iterator))


@pytest.mark.parametrize("inputs, expected_substrings", generate_automated_test_cases())
def test_main_automated(inputs, expected_substrings, monkeypatch, capsys):
    """
    Test the main function with automatically generated test cases.
    """
    from quadratic_equation_solver import main

    # Simulate user inputs
    simulate_inputs(monkeypatch, inputs)

    # Run the main function
    main()

    # Capture and check the output
    captured_output = capsys.readouterr().out

    # Verify expected substrings appear in the output
    for substr in expected_substrings:
        assert substr in captured_output, f"Missing expected output: {substr}"
