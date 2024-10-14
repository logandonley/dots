import json
import os.path
from io import BytesIO
from urllib.error import URLError
from urllib.request import urlopen
from zipfile import ZipFile
from utils import cmd


def get_latest_nerdfonts_release() -> str | None:
    """
    Grab the latest release from nerdfonts.

    :return: latest release | None
    """
    url = "https://api.github.com/repos/ryanoasis/nerd-fonts/releases/latest"
    try:
        with urlopen(url) as resp:
            data = json.loads(resp.read().decode())
        return data["tag_name"]
    except (URLError, json.JSONDecodeError, KeyError) as e:
        print(f"Failed to fetch latest release: {e}")
        return None


def font_exists(font: str) -> bool:
    """
    Check if a font already exists in the system.

    :param font:
    :return:
    """
    fonts_dir = os.path.expanduser(f"~/.local/share/fonts/{font}")
    return os.path.isdir(fonts_dir) and any(
        file.endswith((".ttf", ".otf")) for file in os.listdir(fonts_dir)
    )


def install_nerd_font(font: str, version: str):
    fonts_base_dir = os.path.expanduser("~/.local/share/fonts/")
    font_dir = os.path.join(fonts_base_dir, font)

    if font_exists(font):
        print(f"{font} already exists on system. Skipping.")
        return

    base_url = f"https://github.com/ryanoasis/nerd-fonts/releases/download/{version}/"
    font_url = f"{base_url}{font}.zip"

    print(f"Downloading {font}@{version} from nerd fonts.")

    try:
        with urlopen(font_url) as resp:
            font_data = resp.read()
    except URLError as e:
        print(f"Failed to download {font}: {e}")
        return

    with ZipFile(BytesIO(font_data)) as zip_file:
        os.makedirs(font_dir, exist_ok=True)

        for file in zip_file.namelist():
            zip_file.extract(file, font_dir)

    print(f"{font} installed into {font_dir}")


def update_font_cache():
    """
    Use the local fc-cache tool to generate the font cache files.

    Run this after downloading new fonts.
    :return:
    """
    cmd(["fc-cache"])
