#!/usr/bin/env python3
"""
Bootstraps the full system.

Includes packages, languages, dotfiles, fonts, and more.

> ./bootstrap.py

This is the main entrypoint into this project.
The operations are designed to be idempotent (as much as possible).
"""

import os.path

from yaml import safe_load

from dots import copy_dotfiles
from fonts import (
    get_latest_nerdfonts_release,
    install_nerd_font,
    update_font_cache,
    install_fontsource_font,
)
from git import setup_git
from mise import ensure_mise, mise_use
from omz import ensure_omz
from packages import install_packages, system_update, install_groups
from repos import download_repo


def load_bootstrap_file(file: str):
    """
    Loads the YAMl definition file.

    :param: The source YAML file
    :return: A dict from the yaml file
    """
    with open(file, "r") as f:
        bootstrap_data = safe_load(f)
    return bootstrap_data


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

    ensure_mise()
    languages = data["mise"]
    for language in languages:
        mise_use(language)

    nerd_font_version = get_latest_nerdfonts_release() or "v3.2.1"
    nerd_fonts = data["fonts"]["nerd"]
    for font in nerd_fonts:
        install_nerd_font(font, nerd_font_version)

    fontsource_fonts = data["fonts"]["fontsource"]
    for font in fontsource_fonts:
        install_fontsource_font(font)

    update_font_cache()

    # Recursively go through all contents in the ./home directory and copy into ~
    repo_home = "./home"
    real_home = os.path.expanduser("~")
    copy_dotfiles(repo_home, real_home)


if __name__ == "__main__":
    bootstrap()
