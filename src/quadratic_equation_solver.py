"""
Converted from https://raw.githubusercontent.com/pof-mchliakh/Quadratic-Equation-Solver/refs/heads/master/Quadratic.java
"""

import math

ERROR = 0.00000001  # acceptable error for Newton's Method


class NotEnoughPrecisionException(Exception):
    pass


def solve_quadratic(a, b, c):
    discriminant = b * b - 4 * a * c
    # if math.isnan(discriminant) or discriminant == b * b: TODO: Faulty
    if math.isnan(discriminant):
        raise NotEnoughPrecisionException()

    if discriminant < 0:  # complex roots
        sqrt = sqrt_by_newton(-1 * discriminant)
        real = (-1 * b) / (2 * a)
        imaginary = sqrt / (2 * a)
        return complex(real, imaginary), complex(real, -imaginary)
    else:  # real roots
        sqrt = sqrt_by_newton(discriminant)
        # mixed approach to avoid subtractive cancellation
        q = (-0.5) * (b + sign(b) * sqrt)
        # TODO: Faulty
        # Handle q = 0 to avoid division by zero
        if q == 0:
            if c != 0:
                raise ValueError("Invalid state: q=0 but c≠0.")
            x1 = 0.0
            x2 = -b / a  # Simplified when c = 0
        else:
            x1 = q / a
            x2 = c / q

        return x1, x2


def sign(b):
    """
    Extracts the sign of a double value.
    :param b: the double value
    :return: 1 if the value is positive, -1 if the value is negative
    """
    return 1 if b > 0 else -1


def sqrt_by_newton(value):
    """
    Computes the square root of a number using Newton's Method.
    Returns when the error threshold has been reached.
    :param value: the number to compute the square root of
    :return: the square root of the number
    """
    # square root of zero is zero
    if value == 0:
        return 0

    previous = (1 + value) / 2

    # iterate until error threshold is reached
    while True:
        result = (previous + value / previous) / 2
        if abs(previous - result) < ERROR:
            break
        previous = result

    return result


def format_double(value) -> str:
    """
    Checks whether a double value actually represents an integer,
    and formats accordingly.
    :param value: the double value to format
    :return: the formatted double value
    """
    # check if value is actually an integer
    if math.floor(value) == value:
        return str(int(value))
    else:
        return str(value)


def validate_input(input_str: str):
    """
    Validates the input by converting to type double and inspecting for
    overflow. Throws an exception if overflow occurred.
    :param input_str: the input string
    :return: the double value
    """
    # parse the input
    double_value = float(input_str)

    # append .0 when input is integer
    formatted_str = input_str
    if "." not in input_str:
        formatted_str += ".0"

    # format value to decimal of (almost) arbitrary length
    formatted_double = f"{double_value:.100f}".rstrip("0").rstrip(".")

    if "." not in formatted_double:
        formatted_double += ".0"

    # if new value is not equal to original, overflow has occurred
    if (
        formatted_double != formatted_str and str(double_value) != input_str
    ):  # str() to validation e-notation
        raise NotEnoughPrecisionException()

    return double_value


def main():
    print(
        "Welcome to Quadratic Equation Solver.\n"
        "A quadratic equation can be written in the form ax^2 + bx + c = 0, where x is an unknown, a, b, and c are constants, and a is not zero.\n"
        "Given values for a, b, and c, this program will produce the two roots of the equation. Both real and complex roots are supported, but not complex coefficients.\n"
        "Press Ctrl+C to quit at any time."
    )

    while True:
        # collect input from user
        try:
            a = validate_input(
                input("Enter a value for 'a': ")
            )  # validate before storing
            # make sure a is not zero
            if a == 0:
                print("'a' cannot be zero!")
                continue
            b = validate_input(input("Enter a value for 'b': "))
            c = validate_input(input("Enter a value for 'c': "))
        except NotEnoughPrecisionException:
            print(
                "The value you entered is too large or too small! Please enter a valid number."
            )
            continue
        except ValueError:
            print(
                "The value you entered is not allowed! Please enter a number. E.g. 4, 0.3, -12"
            )
            continue

        # solve equation
        try:
            roots = solve_quadratic(a, b, c)
            x1, x2 = roots

            if isinstance(x1, complex):
                # Display complex roots
                print(f"x1 = {format_double(x1.real)} + {format_double(x1.imag)}i")
                print(f"x2 = {format_double(x2.real)} - {format_double(x2.imag)}i")
            else:
                # Display real roots
                print(f"x1 = {format_double(x1)}")
                if x1 != x2:
                    print(f"x2 = {format_double(x2)}")

        except NotEnoughPrecisionException:
            print(
                "Failed to find an accurate solution! "
                "This can happen when the values are too big, "
                "a is too close to zero, or b^2 is much bigger than 4ac."
            )

        # prompt user
        prompt = input("Would you like to try again? [y/n]: ")
        if prompt.lower() != "y":
            break

    # goodbye
    print("Thank you for using Quadratic Equation Solver!")


if __name__ == "__main__":
    main()
