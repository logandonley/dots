import os

from utils import cmd


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

    cmd(["git", "clone", src, target_dir], error_msg=f"Error fetching '{src}' git repo")
