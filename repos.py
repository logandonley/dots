import os
import subprocess


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
