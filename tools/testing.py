import subprocess

from smolagents import tool


@tool
def run_tests(test_file: str | None) -> str:
    """Run tests using pytest

    Args:
       test_file: (optional) The test file to run.
    """

    # run and capture stdout and stderr
    cmd = 'uv run pytest'
    if test_file:
        cmd += f' {test_file}'

    result = subprocess.run(cmd, shell=True, capture_output=True)
    result_string = f'Out: {result.stdout.decode()}\nErr: {result.stderr.decode()}'
    return result_string
