# quadratic_equation_solver.py
import itertools

# Parameter a
a_categories = {
    # We exclude 0 as a separate special case
    "positive_small": [0.1, 1],
    "positive_large": [100, 1000],
    "negative_small": [-1, -0.1],
    "negative_large": [-100, -1000],
}

# Parameter b
b_categories = {
    "zero": [0],
    "positive_small": [0.1, 1],
    "positive_large": [100, 1000],
    "negative_small": [-1, -0.1],
    "negative_large": [-100, -1000],
}

# Parameter c
c_categories = {
    "zero": [0],
    "positive_small": [0.1, 1],
    "positive_large": [100, 1000],
    "negative_small": [-1, -0.1],
    "negative_large": [-100, -1000],
}

# Special cases
special_cases = [
    (0, 0, 0),  # Zero coefficients
    (0, 0, 1),  # No solution
    (0, 1, 0),  # Linear equation with solution x=0
    (0, 2, 4),  # Linear equation with solution x=-2
    (1, 2, 1),  # Perfect square (one repeated root)
    (4, 4, 1),  # Perfect square with a ≠ 1
]


def generate_test_cases():
    test_cases = []

    # Generate combinations with constraints
    for a_cat, a_val in [
        (cat, val) for cat in a_categories for val in a_categories[cat]
    ]:
        for b_cat, b_val in [
            (cat, val) for cat in b_categories for val in b_categories[cat]
        ]:
            for c_cat, c_val in [
                (cat, val) for cat in c_categories for val in c_categories[cat]
            ]:
                # Create discriminant for checking result type
                discriminant = b_val**2 - 4 * a_val * c_val

                # Tag the test case for expected result type
                if discriminant > 0:
                    tag = "two_real_roots"
                elif discriminant == 0:
                    tag = "one_real_root"
                else:
                    tag = "complex_roots"

                test_cases.append((a_val, b_val, c_val, tag))

    # Add special cases with their expected result tags
    test_cases.extend([*[(a, b, c, "special_case") for a, b, c in special_cases]])

    return test_cases
