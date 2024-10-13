import os.path
import subprocess
from typing import List

from yaml import safe_load


def load_bootstrap_file(file: str):
    """
    Loads the YAMl definition file.

    :param: The source YAML file
    :return: A dict from the yaml file
    """
    with open(file, "r") as f:
        bootstrap_data = safe_load(f)
    return bootstrap_data


def setup_git(config):
    assert config["name"], "Missing git.name definition"
    assert config["email"], "Missing git.email definition"
    assert config["defaultBranch"], "Missing git.defaultBranch definition"
    assert config["autoRemote"], "Missing git.autoRemote definition"

    commands = [
        ["git", "config", "--global", "user.name", config["name"]],
        ["git", "config", "--global", "user.email", config["email"]],
        ["git", "config", "--global", "init.defaultBranch", config["defaultBranch"]],
        ["git", "config", "--global", "push.autoSetupRemote", config["autoRemote"]],
    ]

    for cmd in commands:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(result.stderr)
            raise Exception(
                f"Received return code {result.returncode} when running git operation"
            )


def system_update():
    """
    Run dnf update to make sure everything is upgraded.

    :return:
    """

    result = subprocess.run(
        ["sudo", "dnf", "update", "-y"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when performing system update"
        )


def install_groups(groups: List[str]):
    """
    Perform a `dnf group install` against the target group(s)

    :param groups: The dnf groups to install
    :return:
    """

    result = subprocess.run(
        ["sudo", "dnf", "group", "install", "-y"] + groups,
        capture_output=True,
        text=True,
    )
    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when installing {groups}"
        )


def install_packages(packages: List[str]):
    """
    Perform a `dnf install` against the target package(s)

    :param packages: The dnf packages to install
    :return:
    """

    result = subprocess.run(
        ["sudo", "dnf", "install", "-y"] + packages,
        capture_output=True,
        text=True,
    )
    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"Received return code {result.returncode} when installing {packages}"
        )


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


if __name__ == "__main__":
    bootstrap()
