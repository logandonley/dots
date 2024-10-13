import subprocess


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
