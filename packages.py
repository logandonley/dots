import json
import subprocess
import tempfile
from shutil import which
from typing import List
from urllib.error import URLError
from urllib.request import urlopen

from utils import cmd
import platform


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


def get_latest_release_github(org: str, repo: str):
    url = f"https://api.github.com/repos/{org}/{repo}/releases/latest"

    try:
        with urlopen(url) as resp:
            data = json.loads(resp.read())
    except URLError as e:
        print(f"Failed to get latest release for {org}/{repo}: {e}")
        return

    return data


def get_release_assets(data) -> List[dict]:
    """
    Simple func to return the assets array
    :param data: output from get_latest_release_github
    :return:
    """
    assert "assets" in data, "No assets found in the passed in data."
    return data["assets"]


def get_rpm_asset_url(assets: List[dict], arch: str) -> str | None:
    """
    Grab the URL for the rpm file from the asset based on the system architecture.
    :param assets:
    :param arch: system architecture
    :return: The download URL
    """
    noarch = None
    for asset in assets:
        if asset["name"].endswith(f"{arch}.rpm"):
            return asset["browser_download_url"]
        elif asset["name"].endswith(f"noarch.rpm"):
            noarch = asset["browser_download_url"]

    # fallback to a noarch option if there isn't a match and it is available
    return noarch


def install_rpm_from_url(url: str):
    """
    Download a `.rpm` file from a URL and install it.

    :param url:
    :return:
    """
    try:
        with urlopen(url) as resp:
            data = resp.read()
            with tempfile.NamedTemporaryFile(mode="wb", suffix=".rpm") as f:
                f.write(data)
                f.flush()

                install_packages([f.name])
    except URLError as e:
        print(f"Failed to download {url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def is_program_installed(program: str) -> bool:
    """
    Does a basic check to see if the target program is available on the
    $PATH. This isn't comprehensive, but for the purposes of this tool
    it should be sufficient.

    :param program:
    :return:
    """
    return bool(which(program))


def download_binary_to_bin():
    pass


def get_system_architecture():
    """
    Returns the system architecture.

    Converted into the naming that is common in software releases.
    :return:
    """
    arch = platform.machine().lower()
    if arch in ["x86_64", "amd64"]:
        return "amd64"
    elif arch in ["aarch64", "arm64"]:
        return "arm64"
    else:
        return arch


def ensure_program_from_github(owner: str, repo: str):
    """
    Makes sure that a program from a github repo is installed.

    :param owner:
    :param repo:
    :return:
    """
    # TODO: Should probably support the case where the program name doesn't match the repo name
    if is_program_installed(repo):
        return

    arch = get_system_architecture()
    release = get_latest_release_github(owner, repo)
    assets = get_release_assets(release)
    url = get_rpm_asset_url(assets, arch)
    install_rpm_from_url(url)
    print(f"{repo} installed.")


def install_npm_global_package(package: str):
    pass


if __name__ == "__main__":
    pass
