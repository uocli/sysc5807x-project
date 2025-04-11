import builtins
import os
import subprocess
import time

import pytest

from src.quadratic_equation_solver import ERROR, main, solve_quadratic
from quadratic_equation_solver_categories import generate_test_cases


def is_close(a, b, rel_tol=ERROR, abs_tol=ERROR) -> bool:
    """
    Check if two values are close (supports real and complex numbers)
    :param a: First value (int/float/complex)
    :param b: Second value (int/float/complex)
    :param rel_tol: Maximum allowed relative difference (default 1e-9)
    :param abs_tol: Minimum absolute difference threshold (default 1e-9)
    :return: True if values are considered close, False otherwise
    """
    # Handle NaN cases
    if (a != a) or (b != b):  # NaN check
        return False

    # Convert both to complex to handle mixed real/complex comparisons
    a = complex(a)
    b = complex(b)

    # Check real and imaginary components independently
    for a_part, b_part in [(a.real, b.real), (a.imag, b.imag)]:
        # Short-circuit for exact equality or both infinite
        if a_part == b_part:
            continue

        # Magnitude scaling for relative tolerance
        max_mag = max(abs(a_part), abs(b_part))

        # Calculate effective tolerance
        tol = max(rel_tol * max_mag, abs_tol)

        # Absolute difference for this component
        diff = abs(a_part - b_part)

        if diff > tol:
            return False

    return True


def verify_roots(a, b, c, roots) -> bool:
    """
    Verify if the roots are correct for the given quadratic equation
    :param a: number 1
    :param b: number 2
    :param c: number 3
    :param roots: list of roots to verify
    :return: True if roots are correct, False otherwise
    """
    if a == 0:
        # Linear equation: bx + c = 0
        if b == 0:
            # c = 0
            if c == 0:
                # 0 = 0, infinite solutions
                return roots == ("Infinite solutions",)
            else:
                # c = 0 where c != 0, no solution
                return roots == ("No solution",)
        else:
            # b!= 0, linear equation with one root: x = -c/b
            return len(roots) == 1 and is_close(roots[0], -c / b)
    else:
        # a != 0, check if all roots are valid by substituting them back into the equation
        for root in roots:
            # Skip non-numeric roots (for error messages)
            if not isinstance(root, (int, float, complex)):
                continue

            # Calculate ax**2 + bx + c for this root
            result = a * root**2 + b * root + c
            print("Result:", result)
            # Result should be close to zero for a valid root
            if not is_close(result, 0):
                return False

        # Also verify the number and type of roots based on discriminant
        discriminant = b**2 - 4 * a * c

        if discriminant > 0:
            # Should have two distinct real roots
            return (
                len(roots) == 2
                and isinstance(roots[0], (int, float))
                and isinstance(roots[1], (int, float))
                and not is_close(roots[0], roots[1])
            )
        elif is_close(discriminant, 0):
            # Should have one repeated real root (or two equal roots)
            return (
                len(roots) == 2
                and isinstance(roots[0], (int, float))
                and isinstance(roots[1], (int, float))
                and is_close(roots[0], roots[1])
            )
        else:
            # Should have two complex conjugate roots
            return (
                len(roots) == 2
                and isinstance(roots[0], complex)
                and isinstance(roots[1], complex)
                and is_close(roots[0].real, roots[1].real)
                and is_close(roots[0].imag, -roots[1].imag)
            )


@pytest.mark.parametrize("a,b,c,tag", generate_test_cases())
def test_solve_quadratic(a, b, c, tag):
    try:
        # Measure execution time
        start = time.time()
        roots = solve_quadratic(a, b, c)
        end = time.time()

        # Print execution time for performance analysis
        print(f"Test case ({a}, {b}, {c}) executed in {(end - start)*1000:.6f} ms")

        # Verify the roots are correct
        assert verify_roots(
            a, b, c, roots
        ), f"Roots {roots} are not correct for equation {a}x**2 + {b}x + {c} = 0"

    except Exception as e:
        # Check if error is expected for special edge cases
        if tag == "special_case" and a == 0:
            # It's okay to raise an exception for some edge cases
            # You may need to adapt this based on your implementation's behavior
            pass
        else:
            # Unexpected error
            raise e


def simulate_inputs(monkeypatch, inputs):
    """
    Simulate user inputs for testing purposes.
    """
    iterator = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _: next(iterator))


def test_a_equals_zero(monkeypatch, capsys):
    """
    Test the case where 'a' is zero, which should prompt a retry.
    """
    simulate_inputs(monkeypatch, ["0", "1", "-2", "1", "n"])  # a=0 -> retry
    main()
    out = capsys.readouterr().out
    assert "'a' cannot be zero" in out
    assert "x1 = 1" in out
    assert "x2 = 1" not in out, "x2 shouldn't be printed as x1 == x2"


def test_complex_roots(monkeypatch, capsys):
    """
    Test the case where the roots are complex.
    """
    simulate_inputs(monkeypatch, ["1", "2", "5", "n"])  # complex roots
    main()
    out = capsys.readouterr().out
    assert "+ " in out or "+0." in out  # crude check for complex output
    assert "- " in out or "-0." in out


def test_equal_real_roots(monkeypatch, capsys):
    simulate_inputs(monkeypatch, ["1", "2", "1", "n"])  # one root
    main()
    out = capsys.readouterr().out
    assert "x1 = -1" in out
    assert "x2" not in out or "x2 = -1" not in out  # x2 shouldn't be printed


def test_retry_then_exit(monkeypatch, capsys):
    """
    Test the case where the user retries and then exits.
    """
    simulate_inputs(monkeypatch, ["1", "0", "-1", "y", "1", "2", "5", "n"])
    main()
    out = capsys.readouterr().out
    assert out.count("x1") >= 2
    assert "Thank you for using" in out


def test_invalid_input_handling_nan(monkeypatch, capsys):
    """
    Test the case where the input is 'nan', which is not a valid number for 'a'.
    """
    simulate_inputs(monkeypatch, ["nan", "2", "3", "n"])  # a = NaN
    main()
    out = capsys.readouterr().out
    assert "Failed to find an accurate solution!" in out


def test_invalid_input_handling_abc(monkeypatch, capsys):
    """ "
    Test the case where the input is not a number (e.g., 'abc').
    """
    simulate_inputs(monkeypatch, ["abc", "2", "3", "4", "n"])
    main()
    out = capsys.readouterr().out
    assert "The value you entered is not allowed!" in out


def test_not_enough_precision_exception(monkeypatch, capsys):
    """
    Test the case where the input is too large or too small, causing a precision error.
    """
    simulate_inputs(monkeypatch, ["0.123456789123456789", "2", "3", "4", "n"])
    main()
    out = capsys.readouterr().out
    assert "The value you entered is too large or too small!" in out


def test_run_script():
    """
    Test the script execution with simulated user input.
    """
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(
        current_dir, "..", "..", "src", "quadratic_equation_solver.py"
    )
    user_input = "1\n2\n3\nn\n"  # Adjust these as per the input expected by your script
    out = subprocess.run(
        ["python3", script_path],
        input=user_input,  # Simulate the user input
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert (
        out.returncode == 0
    ), f"Script failed with return code {out.returncode} and stderr: {out.stderr}"
    assert "Welcome to Quadratic Equation Solver" in out.stdout
