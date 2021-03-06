# If not running interactively, don't do anything
[[ $- != *i* ]] && return

exitcolour() {
	if [ $1 -eq 0 ]; then
		echo -n 234
	else
		echo -n 160
	fi
	# Restore exit status
	exit $1
}

#PS1="\[\e[48;5;\$(exitcolour \$?)m\]\$? \[\e[38;5;\$(exitcolour \$?)m\e[48;5;239m\]\[\e[38;5;255m\] \W \[\e[0m\e[38;5;239m\]\$(tput sgr0) "
PS1='$?|\W> '

# Exports
. ~/.exports

# Git auto complete
source /usr/share/git/completion/git-completion.bash

# Aliases
alias mymount='sudo mount -o uid=1000,gid=1000'
alias sshm1='ssh -p 6416 m1cr0man@m1cr0man.com'
alias sship='ssh -i ~/.ssh/id_rsa_irishpressings -L 27017:127.0.0.1:27017 git@172.16.1.122'
alias sshipfwd='ssh -Ni ~/.ssh/id_rsa_irishpressings -L 27017:127.0.0.1:27017 git@172.16.1.122'
alias ls='ls --color=auto'
alias l='ls'
alias c='cd'
alias cb='xclip -selection clipboard'
alias exporteslint='export PATH=$PATH:/home/lucas/Github/vacation/client/node_modules/.bin'
alias chkgpu='sudo cat /sys/kernel/debug/vgaswitcheroo/switch'
alias py='python3'
alias py3='python3'
alias py2='python2.7'
alias diffnice='diff -Naur'

# Consort aliases
alias conlas='consort -D las'
alias contat='consort -D tat'
alias clih='consort -D las show inventory host'
alias clis='consort -D las show inventory settings'

# LS Colours
eval $(dircolors -b "$HOME/.config/m1cr0man/LS_COLOURS")

# TMux
[[ $TERM == 'rxvt'* ]] && exec tmux
