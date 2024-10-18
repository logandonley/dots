export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="cypher"
plugins=(git z)

source $ZSH/oh-my-zsh.sh
export EDITOR="nvim"
alias v=nvim
eval "$(/home/logan/.local/bin/mise activate zsh)"

export PATH=$PATH:"/home/logan/.local/share/JetBrains/Toolbox/scripts/"

alias task="go-task"

# . "$HOME/.cargo/env"
