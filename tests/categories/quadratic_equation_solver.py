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
    for a_category, a_value in [
        (category, value)
        for category in a_categories
        for value in a_categories[category]
    ]:
        for b_category, b_value in [
            (category, value)
            for category in b_categories
            for value in b_categories[category]
        ]:
            for c_category, c_value in [
                (category, value)
                for category in c_categories
                for value in c_categories[category]
            ]:
                # Create discriminant for checking result type
                discriminant = b_value**2 - 4 * a_value * c_value

                # Tag the test case for expected result type
                if discriminant > 0:
                    tag = "two_real_roots"
                elif discriminant == 0:
                    tag = "one_real_root"
                else:
                    tag = "complex_roots"

                test_cases.append((a_value, b_value, c_value, tag))

    # Add special cases with their expected result tags
    test_cases.extend([*[(a, b, c, "special_case") for a, b, c in special_cases]])

    return test_cases
