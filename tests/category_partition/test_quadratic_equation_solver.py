import pytest
import time
from src.quadratic_equation_solver import solve_quadratic, ERROR
from category_partition.quadratic_equation_solver_categories import generate_test_cases


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
