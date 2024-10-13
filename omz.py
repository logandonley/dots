import os
import subprocess
from shutil import which

from packages import install_packages


def get_user() -> str:
    """
    Get the current logged-in user.

    :return: The current logged-in user
    """
    return os.getenv("USER")


def get_login_shell(user: str) -> str:
    """
    Grab the login shell for the targeted user

    :param user: Target linux user
    :return: The login shell
    """
    result = subprocess.run(
        ["grep", user, "/etc/passwd"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when attempting to get login shell"
        )

    line = result.stdout.strip()
    return line.split(":")[-1]


def change_login_shell(user: str, shell: str):
    """
    Change the login shell for the target user.

    :param user: Linux user
    :param shell: Path to the target shell (e.g. /usr/bin/zsh)
    :return:
    """
    result = subprocess.run(
        ["sudo", "chsh", "--shell", shell, user],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when attempting to set login shell '{shell}' for user '{user}'"
        )


def ensure_omz():
    """
    Make sure that Oh My Zsh is setup and zsh is installed.

    :return:
    """
    # First make sure Zsh is installed
    zsh_installed = which("zsh")
    if not zsh_installed:
        install_packages(["zsh"])

    user = get_user()
    login_shell = get_login_shell(user)

    if login_shell != which("zsh"):
        change_login_shell(user, which("zsh"))

    exists = os.path.exists(os.path.expanduser("~/.oh-my-zsh"))
    if exists:
        return

    result = subprocess.run(
        [
            "/bin/bash",
            "-c",
            "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh -s -- --unattended --keep-zshrc",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when attempting to install omz"
        )
