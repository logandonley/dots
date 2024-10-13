import difflib
import os.path
from shutil import which
import subprocess

from yaml import safe_load

from dots import copy_dotfiles
from git import setup_git
from packages import install_packages, system_update, install_groups


def load_bootstrap_file(file: str):
    """
    Loads the YAMl definition file.

    :param: The source YAML file
    :return: A dict from the yaml file
    """
    with open(file, "r") as f:
        bootstrap_data = safe_load(f)
    return bootstrap_data


def download_repo(target: str, src: str):
    """
    Clone the target repo to a location on the filesystem.

    :param target: The target location on the filesystem where you want to clone the repo
    :param src: The git url (https) that contains the repo you want to clone
    :return:
    """
    target_dir = os.path.expanduser(target)

    # Check if it exists
    if os.path.exists(target_dir):
        print(f"{target_dir} already exists. Continuing.")
        return

    result = subprocess.run(
        ["git", "clone", src, target_dir],
        capture_output=True,
        text=True,
    )
    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when installing fetching '{src}' git repo"
        )


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


def bootstrap():
    data = load_bootstrap_file("bootstrap.yaml")

    system_update()

    git_config = data["git"]
    if git_config:
        setup_git(git_config)

    groups = data["groups"]
    if groups:
        install_groups(groups)

    packages = data["packages"]
    if packages:
        install_packages(packages)

    repos = data["repos"]
    for repo in repos:
        download_repo(repo["target"], repo["src"])

    ensure_omz()

    # Recursively go through all contents in the ./home directory and copy into ~
    repo_home = "./home"
    real_home = os.path.expanduser("~")
    copy_dotfiles(repo_home, real_home)


if __name__ == "__main__":
    bootstrap()
