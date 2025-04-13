import timeit
import statistics
import pytest
import io
import contextlib


def run_tests_with_timing(test_module, num_runs=10):
    """
    Run tests multiple times and record their execution times.

    :param test_module: Path to the test module
    :param num_runs: Number of times to run the tests
    :return: A dictionary with timing statistics
    """

    def run_single_test():
        # Use contextlib to capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            # Redirect stdout and stderr
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(
                stderr_capture
            ):
                # Run pytest for the specific module
                result = pytest.main(["-v", test_module])

            # If tests failed, print captured output
            if result != 0:
                print(f"\nTests failed for {test_module} with exit code {result}")
                print("--- Stdout ---")
                print(stdout_capture.getvalue())
                print("--- Stderr ---")
                print(stderr_capture.getvalue())

            return result == 0  # 0 means all tests passed
        except Exception as e:
            print(f"An error occurred while running the tests: {e}")
            return False

    # Measure execution times
    execution_times = []
    for _ in range(num_runs):
        # Use timeit to get the most accurate timing
        execution_time = timeit.timeit(run_single_test, number=1)
        execution_times.append(execution_time)

    # Calculate statistics
    return {
        "total_runs": num_runs,
        "mean": statistics.mean(execution_times),
        "std_dev": statistics.stdev(execution_times) if num_runs > 1 else 0,
    }


# Run timing for both test modules
if __name__ == "__main__":
    test_modules = [
        "tests/category_partition/test_date_format_converter_cp.py",
        "tests/category_partition/test_quadratic_equation_solver_cp.py",
        "tests/metamorphic/test_date_converter_mt.py",
        "tests/metamorphic/test_quadratic_equation_solver_mt.py",
    ]

    for module in test_modules:
        print(f"\nTiming results for {module}:")
        timing_results = run_tests_with_timing(module)

        print("Execution Time Statistics (in seconds):")
        for key, value in timing_results.items():
            print(f"{key}: {value:.4f}")
