import cmath
import math
from unittest.mock import patch
import pytest

from hypothesis import given, strategies as st, settings, note

from src.quadratic_equation_solver import ERROR, solve_quadratic

# Define strategies for generating coefficients
# Avoid values too close to zero for 'a' to prevent linear equations
nonzero_coefficient = st.floats(min_value=-100, max_value=100).filter(
    lambda x: abs(x) > 1e-3
)
any_coefficient = st.floats(min_value=-100, max_value=100)
zero_coefficient = st.just(0.0)
scale_factors = st.floats(min_value=-10, max_value=10).filter(lambda x: abs(x) > 1e-6)


@st.composite
def reasonable_coefficients(draw):
    """
    Strategy to generate stable (a, b, c) tuples for quadratic equations.
    :param draw: the Hypothesis draw function
    :return: a tuple of coefficients (a, b, c)
    """
    # Ensure 'a' is not too small to keep it quadratic
    a = draw(st.floats(min_value=-100, max_value=100).filter(lambda x: abs(x) > 1e-3))

    # Generate b and c in a reasonable range
    b = draw(st.floats(min_value=-100, max_value=100))
    c = draw(st.floats(min_value=-100, max_value=100))

    # Optionally rescale if there's a crazy ratio (optional: based on a heuristic)
    max_coefficient = max(abs(a), abs(b), abs(c))
    if max_coefficient > 0 and (abs(a) / max_coefficient < 1e-6):
        a = math.copysign(1e-3 * max_coefficient, a)  # nudge a toward a safe ratio

    return a, b, c


def is_close(a, b, *, rel_tol=ERROR, abs_tol=ERROR) -> bool:
    """
    Check if two values are close to each other within a tolerance.
    :param a: the first value
    :param b: the second value
    :param rel_tol: the relative tolerance
    :param abs_tol: the absolute tolerance
    :return: True if the values are close, False otherwise
    """
    if isinstance(a, complex) or isinstance(b, complex):
        return cmath.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def roots_satisfy_equation(
    a: (int, float, complex),
    b: (int, float, complex),
    c: (int, float, complex),
    roots: list,
) -> bool:
    """
    Check if the roots satisfy the quadratic equation.
    :param a: the coefficient of x^2
    :param b: the coefficient of x
    :param c: the constant term
    :param roots: the roots to check
    :return: True if the roots satisfy the equation, False otherwise
    """
    for r in roots:
        val = a * r**2 + b * r + c
        if not is_close(val, 0):
            print(f"Root {r} yields value {val}, which is not close to 0.")
            return False
    return True


@settings(max_examples=100)
@given(a=nonzero_coefficient, b=any_coefficient, c=any_coefficient, scale=scale_factors)
def test_mr1_coefficient_scale(a, b, c, scale):
    """
    Test metamorphic relation: scaling coefficients.
    :param a: the coefficient of x^2
    :param b: the coefficient of x
    :param c: the constant term
    :param scale: the scaling factor
    """
    note(f"Testing coefficients a={a}, b={b}, c={c} with scale={scale}")

    # Get roots with original and scaled coefficients
    original_roots = solve_quadratic(a, b, c)
    scaled_roots = solve_quadratic(a * scale, b * scale, c * scale)

    # Verify both sets of roots satisfy their respective equations
    assert roots_satisfy_equation(
        a, b, c, original_roots
    ), f"Original roots {original_roots} don't satisfy equation {a}x^2 + {b}x + {c} = 0"

    assert roots_satisfy_equation(
        a * scale, b * scale, c * scale, scaled_roots
    ), f"Scaled roots {scaled_roots} don't satisfy equation {a*scale}x^2 + {b*scale}x + {c*scale} = 0"


def test_q_zero_and_c_nonzero_metaphorically():
    """
    Test the case where q=0 but c is not 0 for branch coverage
    :return:
    """
    a = 1.0
    b = 2.0
    c = 1.0
    with patch(
        "src.quadratic_equation_solver.sqrt_by_newton", return_value=-2.0
    ), patch("src.quadratic_equation_solver.sign", return_value=1):

        with pytest.raises(ValueError, match="q == 0 but c != 0"):
            solve_quadratic(a, b, c)


@settings(max_examples=100)
@given(coefficients=reasonable_coefficients())
def test_mr2_root_verification(coefficients: tuple):
    """
    Test metamorphic relation: root verification.
    :param coefficients: a tuple of coefficients (a, b, c)
    """
    a, b, c = coefficients  # Unpack the tuple here
    note(f"Testing coefficients a={a}, b={b}, c={c}")

    # Get roots
    roots = solve_quadratic(a, b, c)

    # Verify roots satisfy the equation
    assert roots_satisfy_equation(
        a, b, c, roots
    ), f"Roots {roots} don't satisfy equation {a}x^2 + {b}x + {c} = 0"


@settings(max_examples=100)
@given(coefficients=reasonable_coefficients())
def test_mr3_vieta_formulas(coefficients):
    """
    Test metamorphic relation: Vieta's formulas.
    :param coefficients: a tuple of coefficients (a, b, c)
    """
    a, b, c = coefficients  # Unpack the tuple here
    note(f"Testing coefficients a={a}, b={b}, c={c}")

    # Get roots
    roots = solve_quadratic(a, b, c)

    # Check Vieta's formulas
    sum_of_roots = sum(roots)
    product_of_roots = roots[0] * roots[1]

    assert is_close(
        sum_of_roots, -b / a
    ), f"Sum of roots {sum_of_roots} doesn't equal -b/a = {-b / a}"
    assert is_close(
        product_of_roots, c / a
    ), f"Product of roots {product_of_roots} doesn't equal c/a = {c / a}"


@settings(max_examples=20)
@given(b=nonzero_coefficient, c=any_coefficient)
def test_mr4_linear_equation(b, c):
    """
    Test metamorphic relation: linear equation case (a=0).
    :param b: the coefficient of x
    :param c: the constant term
    """
    note(f"Testing linear equation with b={b}, c={c}")

    # Get roots for linear equation
    roots = solve_quadratic(0, b, c)

    # Should be a single root equal to -c/b
    if b != 0:
        assert len(roots) == 2, f"Linear equation should have 2 roots, got {len(roots)}"
        assert (
            roots[0] == roots[1]
        ), f"Roots should be equal, got {roots[0]} and {roots[1]}"
        assert is_close(
            roots[0], -c / b
        ), f"Root {roots[0]} doesn't equal -c/b = {-c / b}"


def test_edge_cases():
    """
    Test specific edge cases that might be problematic.
    """
    # Perfect square trinomial
    roots = solve_quadratic(1, -2, 1)
    assert len(roots) == 2, f"Expected 2 roots, got {len(roots)}"
    assert is_close(roots[0], 1) and is_close(
        roots[1], 1
    ), f"Roots should be 1 and 1, got {roots}"

    # Equal roots of opposite sign
    roots = solve_quadratic(1, 0, -4)
    assert len(roots) == 2, f"Expected 2 roots, got {len(roots)}"
    assert (is_close(roots[0], 2) and is_close(roots[1], -2)) or (
        is_close(roots[0], -2) and is_close(roots[1], 2)
    ), f"Roots should be 2 and -2, got {roots}"
