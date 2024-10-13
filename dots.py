import difflib
import os
from datetime import datetime
from shutil import copy2


def get_last_modified(file_path: str) -> datetime:
    """
    Find when a given file was last modified.

    :param file_path: Path to the file to examine
    :return: last modified timestamp
    """
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def show_diff(file1: str, file2: str):
    """
    Show the diff between two files

    :param file1: Base file
    :param file2: Possibly changed file to compare
    :return:
    """
    with open(file1, "r") as f1, open(file2, "r") as f2:
        diff = difflib.unified_diff(
            f1.readlines(),
            f2.readlines(),
            fromfile=file1,
            tofile=file2,
        )
        for line in diff:
            print(line, end="")


def copy_dotfiles(repo_home: str, user_home: str):
    """
    Go through all files in the dot files root and copy into the user's home directory

    :param repo_home: The root path to the dot files to copy over
    :param user_home: The user's home directory
    :return:
    """
    for root, dirs, files in os.walk(repo_home):
        for file in files:
            repo_file = os.path.join(root, file)
            real_file = os.path.join(
                user_home,
                os.path.relpath(repo_file, repo_home),
            )

            if os.path.exists(real_file):
                repo_time = get_last_modified(repo_file)
                real_time = get_last_modified(real_file)

                if real_time > repo_time:
                    print(f"\nFile {real_file} is newer than {repo_file}")
                    show_diff(repo_file, real_file)

                    choice = input(
                        "What would you like to do? [o]verwrite, [c]opy to source, [s]kip, [q]uit: "
                    ).lower()

                    if choice == "o":
                        copy2(repo_file, real_file)
                        print(f"Overwrote {real_file}")
                    elif choice == "c":
                        copy2(real_file, repo_file)
                        print(f"Copied {real_file} to {repo_file}")
                    elif choice == "s":
                        print("Skipped")
                    elif choice == "q":
                        return
                    else:
                        print("Invalid choice, skipping")
                else:
                    copy2(repo_file, real_file)
                    print(f"Copied {repo_file} to {real_file}")
            else:
                os.makedirs(os.path.dirname(real_file), exist_ok=True)
                copy2(repo_file, real_file)
                print(f"Copied {repo_file} to {real_file}")


if __name__ == "__main__":
    dotfiles = "./home"
    home = os.path.expanduser("~")
    copy_dotfiles(dotfiles, home)
