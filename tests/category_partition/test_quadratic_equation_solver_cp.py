import builtins
import pytest

from quadratic_equation_solver import main


def generate_main_test_cases():
    # ----------------------------------------------------------------
    # Normal Cases
    # ----------------------------------------------------------------
    # Standard quadratic equations
    yield (
        ["1", "-3", "2", "n"],  # x^2 - 3x + 2 = 0 -> x=2, x=1
        ["x1 = 2", "x2 = 1", "Thank you"],
    )
    yield (
        ["1", "0", "-4", "n"],  # x^2 - 4 = 0 -> x=2, x=-2
        ["x1 = 2", "x2 = -2"],
    )
    # Solve two equations in sequence
    yield (
        ["1", "-3", "2", "y", "1", "2", "5", "n"],
        ["x1 = 2", "x2 = 1", "-1+2j", "-1-2j", "Thank you"],
    )
    # ----------------------------------------------------------------
    # Edge Cases
    # ----------------------------------------------------------------
    # Tiny 'a' value (near-zero)
    yield (
        ["1e-15", "1", "1", "n"],  # 1e-15x^2 + x + 1 = 0
        ["x1 = -999999999999998.9"],
    )
    # Massive coefficients
    yield (
        [
            "1e100",
            "1000000000000000",
            "2000000000000000",
            "1000000000000000",
            "n",
        ],  # Invalid -> valid
        ["too large", "x1 = -1"],
    )
    # Continue after precision error
    yield (
        ["1e200", "1", "0", "0", "y", "1", "0", "0", "n"],
        # Extreme a -> 'y' -> valid
        ["too large", "x1 = 0"],
    )
    # ----------------------------------------------------------------
    # Boundary Conditions
    # ----------------------------------------------------------------
    # Discriminant exactly zero
    yield (
        ["1", "2", "1", "n"],  # (x + 1)^2=0
        ["x1 = -1"],
    )
    # Discriminant near zero (1e-15 difference)
    yield (
        ["1", "2", "1.000000000000001", "n"],  # b^2 - 4ac = -4e-15
        ["j"],  # Complex roots
    )
    # ----------------------------------------------------------------
    # Special Cases
    # ----------------------------------------------------------------
    # Linear equation (a=0) with recovery
    yield (
        ["0", "1", "-2", "1", "n"],  # First a = 0 -> retry
        ["'a' cannot be zero", "x1 = 1"],
    )
    # ----------------------------------------------------------------
    # Input Validation
    # ----------------------------------------------------------------
    # Non-numeric input recovery
    yield (
        ["abc", "1", "2", "1", "n"],
        ["not allowed", "x1 = -1"],
    )
    # NaN handling
    yield (
        ["nan", "1", "1", "n"],
        ["Failed to find an accurate solution"],
    )
    # ----------------------------------------------------------------
    # Mixed Error Handling
    # ----------------------------------------------------------------
    # Multiple errors followed by success
    yield (
        ["0", "a", "0.1", "nan", "1e500", "1", "-3", "2", "n"],
        ["'a' cannot be zero", "not allowed", "too large", "x1 = 2"],
    )


def simulate_inputs(monkeypatch, inputs):
    """Simulate user inputs for testing."""
    iterator = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _: next(iterator))


@pytest.mark.parametrize("inputs, expected_substrings", generate_main_test_cases())
def test_main_edge_cases(inputs, expected_substrings, monkeypatch, capsys):
    """
    Test the main function of the quadratic equation solver.
    :param inputs: the inputs to simulate
    :param expected_substrings: the expected substrings in the output
    :param monkeypatch: the monkeypatch fixture to simulate inputs
    :param capsys: the capsys fixture to capture output
    """
    simulate_inputs(monkeypatch, inputs)
    main()
    captured_output = capsys.readouterr().out

    # Custom checks for special conditions
    for substr in expected_substrings:
        assert substr in captured_output, f"Missing: {substr}"
