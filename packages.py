import subprocess
from typing import List


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
