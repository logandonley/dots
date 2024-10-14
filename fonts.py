import json
import os.path
from io import BytesIO
from urllib.error import URLError
from urllib.request import urlopen, Request
from zipfile import ZipFile

from utils import cmd

FONTS_DIR = os.path.expanduser("~/.local/share/fonts/")


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
    fonts_dir = os.path.join(FONTS_DIR, font)
    return os.path.isdir(fonts_dir) and any(
        file.endswith((".ttf", ".otf")) for file in os.listdir(fonts_dir)
    )


def install_nerd_font(font: str, version: str):
    font_dir = os.path.join(FONTS_DIR, font)

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


def install_fontsource_font(font: str):
    """
    Download a font from fontsource.org if it doesn't already exist on your machine.
    :param font: Font name
    :return:
    """
    formatted_font = font.replace(" ", "")
    font_dir = os.path.join(FONTS_DIR, formatted_font)

    if font_exists(formatted_font):
        print(f"{font} already exists on system. Skipping.")
        return

    font_details_url = (
        f"https://api.fontsource.org/v1/fonts?family={font.replace(' ', '%20')}"
    )
    # Even though it their API is unauthenticated, I think their CDN is blocking
    # requests without headers.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    req = Request(font_details_url, headers=headers)
    try:
        with urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        font_id = data[0]["id"]
    except (URLError, json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Failed to find font {font} from fontsource. \n{e}")
        return

    download_url = f"https://r2.fontsource.org/fonts/{font_id}@latest/download.zip"

    req = Request(download_url, headers=headers)

    try:
        with urlopen(req) as resp:
            font_data = resp.read()
    except URLError as e:
        print(f"Failed to download {font}: {e}")
        return

    with ZipFile(BytesIO(font_data)) as zip_file:
        os.makedirs(font_dir, exist_ok=True)

        for file in zip_file.namelist():
            if file.startswith("ttf/") and "latin" in file:
                content = zip_file.read(file)
                filename = os.path.basename(file)

                with open(os.path.join(font_dir, filename), "wb") as f:
                    f.write(content)
            elif file == "LICENSE":
                zip_file.extract(file, font_dir)

    print(f"{font} installed into {font_dir}")
