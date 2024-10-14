import subprocess
import tempfile
from typing import List
from utils import cmd


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


def install_dnf_repo(repo: dict):
    """
    Installs a dnf repo based on either a source url or a file/content pair.

    Example (yaml):
        url: "https://pkgs.tailscale.com/stable/fedora/tailscale.repo"

        or

        file: "kubernetes.repo"
        content: |
            name=Kubernetes
            baseurl=https://pkgs.k8s.io/core:/stable:/v1.31/rpm/
            enabled=1
            gpgcheck=1
            gpgkey=https://pkgs.k8s.io/core:/stable:/v1.31/rpm/repodata/repomd.xml.key

    :param repo:
    :return:
    """
    if "url" in repo:
        cmd(["sudo", "dnf", "config-manager", "--add-repo", repo["url"]])
        return
    elif "file" in repo and "content" in repo:
        with tempfile.NamedTemporaryFile(mode="w") as tmp_file:
            tmp_file.write(repo["content"])
            tmp_file.flush()

            dst_path = f"/etc/yum.repos.d/{repo['file']}"
            cmd(["sudo", "mv", tmp_file.name, dst_path])
            cmd(["sudo", "chmod", "644", dst_path])

    else:
        print(
            f"Skipping repo {repo}. It is missing required keys of 'url' or 'file' and 'content'"
        )
