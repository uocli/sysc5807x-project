import os
import subprocess


def test_run_script():
    """
    Test the script execution with simulated user input.
    """
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, "..", "src", "date_format_converter.py")
    out = subprocess.run(
        ["python3", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
