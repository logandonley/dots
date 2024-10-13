import os
import subprocess
from shutil import which


def ensure_mise():
    """
    Make sure that mise is installed.

    :return:
    """
    mise_cli_available = which("mise")
    if mise_cli_available:
        print("mise is available.")
        return

    exists = os.path.exists(os.path.expanduser("~/.local/bin/mise"))
    if exists:
        print(
            "mise currently exists at ~/.local/bin/mise but it isn't available on the path."
        )
        return

    install_mise()


def install_mise():
    """
    Installs the mise tool using their installer script.
    :return:
    """
    result = subprocess.run(
        [
            "/bin/bash",
            "-c",
            "curl https://mise.run | sh",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when attempting to install mise"
        )


def mise_use(lang: str):
    result = subprocess.run(
        [
            os.path.expanduser("~/.local/bin/mise"),
            "use",
            "--global",
            lang,
            "-y",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when attempting to install mise"
        )
    print(result.stdout)
