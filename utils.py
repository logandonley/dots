import subprocess
from typing import List


def cmd(args: List[str], error_msg=None) -> str:
    """
    Execute a command line operation.

    :param args: A list of arguments to run. e.g. ["ls", "-latr"]
    :param error_msg: (optional) An additional error message to include in the event of a failure.
    :return: The stdout response from the command
    """
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"Received return code {result.returncode}.\n{error_msg}")
    return result.stdout
