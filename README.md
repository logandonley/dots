# dots

My dotfile and system bootstrapping tool.

## Configuration

Modify `bootstrap.yaml` to suit your needs. This contains the packages, fonts, language runtimes, and more to setup and install.

Add your desired dotfiles into the `./home` directory in the same structure as you want in your `$HOME` directory.

## Running it

```shell
# This runs the entire end-to-end setup
./bootstrap.py
```

```shell
# If you just want to update the dotfiles run
./dots.py
```

## TODOs

- [ ] Cargo install
  - [ ] Stylua install (https://github.com/JohnnyMorganz/StyLua)
- [ ] Random tar.gz file install
- [ ] Install sddm theme
- [ ] Install gtk theme
- [ ] Install gtk icon pack
- [ ] Install cursor theme
- [ ] (maybe) programmatically setup gtk theme config for all relevant files
      This would conflict with the dotfiles, so need to think this through
- [ ] Enable services (e.g. tailscale)
