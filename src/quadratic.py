"""
Converted from https://raw.githubusercontent.com/pof-mchliakh/Quadratic-Equation-Solver/refs/heads/master/Quadratic.java
"""
import math

ERROR = 0.00000001  # acceptable error for Newton's Method


class NotEnoughPrecisionException(Exception):
    pass


class NumberFormatException(Exception):
    pass


def solve_quadratic(a, b, c):
    discriminant = b * b - 4 * a * c
    if math.isnan(discriminant) or discriminant == b * b:
        raise NotEnoughPrecisionException()

    if discriminant < 0:  # complex roots
        sqrt = sqrt_by_newton(-1 * discriminant)
        real = format_double((-1 * b) / (2 * a))
        imaginary = format_double(sqrt / (2 * a))
        # don't print redundant zeros and signs
        output = "x1 = "
        output += real + " + " if real != "0" else ""
        output += imaginary if imaginary != "1" else ""
        output += "i\nx2 = "
        output += real + " - " if real != "0" else "-"
        output += imaginary if imaginary != "1" else ""
        output += "i"
        print(output)
    else:  # real roots
        sqrt = sqrt_by_newton(discriminant)
        # mixed approach to avoid subtractive cancellation
        q = (-0.5) * (b + sign(b) * sqrt)
        x1 = format_double(q / a)
        x2 = format_double(c / q)
        # don't print the same root twice
        output = "x1 = " + x1
        output += "\nx2 = " + x2 if x1 != x2 else ""
        print(output)


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


def format_double(value):
    """
    Checks whether a double value actually represents an integer,
    and formats accordingly.
    :param value: the double value to format
    :return: the formatted double value
    """
    try:
        # check if value is actually an integer
        if math.floor(value) == value:
            return str(int(value))
        else:
            return str(value)
    except Exception:
        raise NumberFormatException()


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
    formatted_double = f"{double_value:.100f}".rstrip('0').rstrip('.')

    if "." not in formatted_double:
        formatted_double += ".0"

    # if new value is not equal to original, overflow has occurred
    if formatted_double != formatted_str and str(double_value) != input_str:  # str() to validation e-notation
        raise NotEnoughPrecisionException()

    return double_value


def main():
    print("Welcome to Quadratic Equation Solver.\n"
          "A quadratic equation can be written in the form ax^2 + bx + c = 0, where x is an unknown, a, b, and c are constants, and a is not zero.\n"
          "Given values for a, b, and c, this program will produce the two roots of the equation. Both real and complex roots are supported, but not complex coefficients.\n"
          "Press Ctrl+C to quit at any time.")

    while True:
        # collect input from user
        try:
            a = validate_input(input("Enter a value for 'a': "))  # validate before storing
            # make sure a is not zero
            if a == 0:
                print("'a' cannot be zero!")
                continue
            b = validate_input(input("Enter a value for 'b': "))
            c = validate_input(input("Enter a value for 'c': "))
        except NotEnoughPrecisionException:
            print("The value you entered is too large or too small! Please enter a valid number.")
            continue
        except NumberFormatException:
            print("The value you entered is not allowed! Please enter a number. E.g. 4, 0.3, -12")
            continue

        # solve equation
        try:
            solve_quadratic(a, b, c)
        except NotEnoughPrecisionException:
            print(
                "Failed to find an accurate solution! "
                "This can happen when the values are too big, "
                "a is too close to zero, or b^2 is much bigger than 4ac."
            )

        # prompt user
        prompt = input("Would you like to try again? [y/n]: ")
        if prompt.lower() != 'y':
            break

    # goodbye
    print("Thank you for using Quadratic Equation Solver!")


if __name__ == "__main__":
    main()
