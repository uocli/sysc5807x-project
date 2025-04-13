import io
import re
from contextlib import redirect_stdout

from hypothesis import given, strategies as st, settings, note, assume
from unittest.mock import patch
import numpy as np

from quadratic_equation_solver import main


complex_pattern = re.compile(r"[+-]?\d*\.?\d+j")


# Define strategies for generating coefficients
real_coefficient = st.floats(min_value=-100, max_value=100).filter(
    lambda x: abs(x) > 0.001
)
nonzero_coefficient = st.floats(min_value=-100, max_value=100).filter(
    lambda x: abs(x) > 0.001
)
any_coefficient = st.one_of(st.just(0.0), real_coefficient)


# Define composite strategies for different equation types
@st.composite
def real_distinct_roots_inputs(draw):
    """Generate inputs that will produce real distinct roots"""
    a = draw(nonzero_coefficient)
    b = draw(real_coefficient)

    # Ensure discriminant is positive by making c appropriately
    # For b^2 - 4ac > 0, we need c < b^2 / 4a
    discriminant_margin = draw(st.floats(min_value=0.1, max_value=10))

    # Calculate c to ensure positive discriminant
    if a > 0:
        c_max = (b**2) / (4 * a) - discriminant_margin
        c = draw(st.floats(max_value=c_max, min_value=-50))
    else:
        c_min = (b**2) / (4 * a) + discriminant_margin
        c = draw(st.floats(min_value=c_min, max_value=50))

    # Convert to strings for input mocking
    return [str(a), str(b), str(c), "n"]


@st.composite
def complex_roots_inputs(draw):
    """Generate coefficients (a, b, c) ensuring complex roots (b^2 < 4ac)"""
    # Generate b first
    b = draw(st.floats(min_value=-50, max_value=50, exclude_min=True, exclude_max=True))

    # Calculate minimum 'a' to ensure c_min <= 50
    a_min = (abs(b) ** 2 + 1) / 200 + 1e-10  # Buffer ensures a > a_min_math
    a = draw(st.floats(min_value=a_min, max_value=50).filter(lambda x: abs(x) > 1e-3))

    # Calculate c_min and ensure it's <=50.0
    c_min = (b**2 + 1) / (4 * a)
    assume(c_min <= 50.0)  # Skip invalid cases due to floating-point errors

    c = draw(st.floats(min_value=c_min, max_value=50))
    return [str(a), str(b), str(c), "n"]


@st.composite
def repeated_roots_inputs(draw):
    """Generate inputs that will produce repeated roots"""
    a = draw(nonzero_coefficient)
    b = draw(real_coefficient)

    # For repeated roots, discriminant must be zero: b^2 = 4ac
    # So c = b^2/4a
    c = (b**2) / (4 * a)

    # Convert to strings for input mocking
    return [str(a), str(b), str(c), "n"]


@st.composite
def special_case_inputs(draw):
    """Generate inputs that test special cases"""
    case_type = draw(
        st.sampled_from(
            [
                "zero_q",  # q = 0 cases
                "a_near_zero",  # a close to 0 (almost linear equation)
                "c_zero",  # c = 0 cases
                "invalid_a",  # a = 0 (invalid)
            ]
        )
    )

    if case_type == "zero_q":
        # For q = (-0.5) * (b + sign(b) * sqrt(b*b - 4*a*c)) to be 0,
        # we need b = 0 and c = 0
        a = draw(nonzero_coefficient)
        return [str(a), "0", "0", "n"]

    elif case_type == "a_near_zero":
        # Very small a, testing handling of nearly linear equations
        a = draw(st.floats(min_value=1e-8, max_value=1e-6))
        b = draw(nonzero_coefficient)
        c = draw(real_coefficient)
        return [str(a), str(b), str(c), "n"]

    elif case_type == "c_zero":
        # c = 0 cases, one root should be 0
        a = draw(nonzero_coefficient)
        b = draw(nonzero_coefficient)
        return [str(a), str(b), "0", "n"]

    else:  # invalid_a
        # a = 0, should be rejected
        valid_a = draw(nonzero_coefficient)
        b = draw(real_coefficient)
        c = draw(real_coefficient)
        # First try a=0, then valid a
        return ["0", str(valid_a), str(b), str(c), "n"]


@st.composite
def error_case_inputs(draw):
    """Generate inputs that will trigger error handling"""
    error_type = draw(
        st.sampled_from(["invalid_format", "extreme_values", "multiple_errors"])
    )

    if error_type == "invalid_format":
        # First an invalid input, then valid inputs
        a = draw(nonzero_coefficient)
        b = draw(real_coefficient)
        c = draw(real_coefficient)
        return ["abc", str(a), str(b), str(c), "n"]

    elif error_type == "extreme_values":
        # Very large values that might cause precision issues
        a = draw(st.sampled_from(["1e100", "1e200"]))
        b = draw(st.sampled_from(["1e100", "1e200"]))
        c = draw(st.sampled_from(["1e100", "1e200"]))
        # Then valid inputs
        valid_a = draw(nonzero_coefficient)
        valid_b = draw(real_coefficient)
        valid_c = draw(real_coefficient)
        return [a, b, c, str(valid_a), str(valid_b), str(valid_c), "n"]

    else:  # multiple_errors
        # Multiple different errors in sequence
        valid_a = draw(nonzero_coefficient)
        valid_b = draw(real_coefficient)
        valid_c = draw(real_coefficient)
        # String of inputs with various errors
        return ["abc", "1e500", str(valid_a), str(valid_b), str(valid_c), "n"]


@st.composite
def consecutive_equations_inputs(draw):
    """Generate inputs for solving multiple equations in sequence"""
    # First equation
    a1 = draw(nonzero_coefficient)
    b1 = draw(real_coefficient)
    c1 = draw(real_coefficient)

    # Second equation
    a2 = draw(nonzero_coefficient)
    b2 = draw(real_coefficient)
    c2 = draw(real_coefficient)

    # Solve first, then solve second, then exit
    return [str(a1), str(b1), str(c1), "y", str(a2), str(b2), str(c2), "n"]


def run_main_with_inputs(inputs):
    # Join inputs with newlines and add a trailing newline to avoid blocking
    input_str = "\n".join(inputs) + "\n"
    input_stream = io.StringIO(input_str)
    output_stream = io.StringIO()

    # Patch sys.stdin to use our input stream
    with patch("sys.stdin", input_stream), redirect_stdout(output_stream):
        main()

    return output_stream.getvalue()


# Metamorphic tests using Hypothesis
@settings(max_examples=10)
@given(inputs=real_distinct_roots_inputs())
def test_mr1_real_roots(inputs):
    """Test handling of equations with real distinct roots"""
    note(f"Testing with inputs: {inputs}")
    output = run_main_with_inputs(inputs)
    # Check that we have two root lines
    assert "x1 = " in output
    assert "x2 = " in output
    # Real roots shouldn't have 'j'
    assert not complex_pattern.search(output)


@settings(max_examples=10)
@given(inputs=complex_roots_inputs())
def test_mr2_complex_roots(inputs):
    """Test handling of equations with complex roots"""
    note(f"Testing with inputs: {inputs}")
    output = run_main_with_inputs(inputs)

    # Check for complex roots
    assert complex_pattern.search(output)


@settings(max_examples=10)
@given(inputs=repeated_roots_inputs())
def test_mr3_repeated_roots(inputs):
    """Test handling of equations with repeated roots"""
    note(f"Testing with inputs: {inputs}")
    output = run_main_with_inputs(inputs)

    # Should only show one root
    assert "x1 = " in output


@settings(max_examples=10)
@given(inputs=special_case_inputs())
def test_mr4_special_cases(inputs):
    """Test special cases that exercise specific branches"""
    note(f"Testing with inputs: {inputs}")
    output = run_main_with_inputs(inputs)

    if "0" == inputs[0]:
        # If first input is a=0, should see rejection message
        assert "'a' cannot be zero" in output

    # Should eventually solve an equation
    assert "x1 = " in output


@settings(max_examples=10)
@given(inputs=error_case_inputs())
def test_mr5_error_handling(inputs):
    """Test error handling paths"""
    note(f"Testing with inputs: {inputs}")
    output = run_main_with_inputs(inputs)

    # Check for error messages based on input type
    if "abc" in inputs:
        assert "not allowed" in output

    if "1e100" in inputs or "1e200" in inputs or "1e500" in inputs:
        assert "large" in output

    # Should eventually solve an equation
    assert "x1 = " in output


@settings(max_examples=10)
@given(inputs=consecutive_equations_inputs())
def test_mr6_multiple_equations(inputs):
    """Test solving multiple equations in sequence"""
    note(f"Testing with inputs: {inputs}")
    output = run_main_with_inputs(inputs)

    # Should solve at least two equations (count occurrences of x1)
    assert output.count("x1 = ") == 2
    # Should have asked "try again" once
    assert "try again" in output


def parse_roots(output):
    """Extract roots from program output as complex numbers"""
    roots = []

    # Find all root lines (x1 = ... and x2 = ...)
    root_lines = re.findall(r"x[12] = (.+)", output)

    for line in root_lines:
        try:
            roots.append(complex(line))
        except ValueError:
            # Handle real roots (e.g., "x1 = 3.0")
            try:
                roots.append(complex(float(line), 0))
            except ValueError:
                # Handle edge cases like "x1 = 0.0 + 0.0i" becoming "0.0+0.0j"
                roots.append(complex(line.replace("j", "")))

    # Sort roots to avoid order mismatches
    return sorted(roots, key=lambda x: (x.real, x.imag))


@settings(max_examples=10)
@given(
    a=nonzero_coefficient,
    b=real_coefficient,
    c=real_coefficient,
    scale=st.floats(min_value=0.5, max_value=2).filter(lambda x: abs(x) > 0.1),
)
def test_mr7_coefficient_scaling(a, b, c, scale):
    """Test that scaling coefficients doesn't change roots"""
    original_output = run_main_with_inputs([str(a), str(b), str(c), "n"])
    scaled_output = run_main_with_inputs(
        [str(a * scale), str(b * scale), str(c * scale), "n"]
    )

    # Check for solution existence
    assert "x1 = " in original_output
    assert "x1 = " in scaled_output

    # Parse and compare roots
    original_roots = parse_roots(original_output)
    scaled_roots = parse_roots(scaled_output)

    assert len(original_roots) == len(scaled_roots)
    for orig, scaled in zip(original_roots, scaled_roots):
        assert np.isclose(orig.real, scaled.real, atol=1e-9)
        assert np.isclose(orig.imag, scaled.imag, atol=1e-9)


def test_edge_cases():
    """Test specific edge cases that might be missed by Hypothesis"""

    # Test case 1: q=0 and c=0 case (simplified equation x^2 = 0)
    inputs1 = ["1", "0", "0", "n"]
    output1 = run_main_with_inputs(inputs1)
    assert "x1 = 0" in output1

    # Test case 2: q=0 but c≠0 case (should trigger ValueError or handle specially)
    inputs2 = ["1", "0", "1", "y", "1", "-3", "2", "n"]
    output2 = run_main_with_inputs(inputs2)
    # First part should have roots ±i
    assert complex_pattern.search(output2)

    # Test case 3: Extreme small values that are valid but challenging
    inputs3 = ["0.001", "1", "0", "n"]
    output3 = run_main_with_inputs(inputs3)
    assert "x1 = 0" in output3 or "x2 = 0" in output3


def test_nan_discriminant_branch():
    """
    Test the specific branch that handles NaN discriminant.
    This directly tests the 'math.isnan(discriminant)' branch.
    """
    # NaN can result from operations like 0/0 or sqrt(-1)
    # For the discriminant b^2-4ac to be NaN, we can use inputs that create NaN

    # Method 1: Using "nan" string directly
    inputs1 = ["1", "nan", "1", "y", "1", "-3", "2", "n"]
    output1 = run_main_with_inputs(inputs1)

    # Check that it handles the NaN case and recovers
    assert (
        "precision" in output1.lower()
        or "accurate solution" in output1.lower()
        or "EXCEPTION:" in output1
    )
    assert "x1 = " in output1  # Should recover and solve valid equation

    # Method 2: Using operations that produce NaN (like 0/0)
    # This might be harder to inject directly, but we can try values known to cause problems
    inputs2 = ["0/0", "1", "1", "1", "-3", "2", "n"]
    output2 = run_main_with_inputs(inputs2)

    # Should either parse as invalid or handle NaN if it gets through
    assert (
        "not allowed" in output2.lower()
        or "precision" in output2.lower()
        or "EXCEPTION:" in output2
    )
    assert "x1 = " in output2  # Should recover and solve valid equation
