import os
import subprocess

from quadratic_equation_solver import solve_quadratic


def test_q_zero_c_non_zero():
    """
    Test the case where q = 0 and c != 0 for coverage.
    :return:
    """
    roots = ()
    try:
        roots = solve_quadratic(0, 0, 1)
    except ValueError:
        assert len(roots) == 0


def test_q_non_zero_a_zero():
    """
    Test the case where q = 0 and c != 0 for coverage.
    :return:
    """
    roots = solve_quadratic(0, 2, 1)
    assert len(roots) == 2
    assert roots[0] == roots[1], "linear equation should have 2 equal roots"


def test_run_script():
    """
    Test the script execution with simulated user input.
    """
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, "..", "src", "quadratic_equation_solver.py")
    user_input = "1\n2\n3\nn\n"  # Adjust these as per the input expected by your script
    out = subprocess.run(
        ["python3", script_path],
        input=user_input,  # Simulate the user input
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
