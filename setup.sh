#!/usr/bin/env bash

echo "Setting up Neovim"
cp -r .config/nvim ~/.config/nvim

# Download vim-plug
mkdir -p ~/.config/nvim/autoload
cd ~/.config/nvim/autoload
wget https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
cd -

echo "Setting up Tmux"
cp .tmux.conf ~/.tmux.conf

# Clone repos for plugins
mkdir -p ~/.config/.tmux/plugins
git clone https://github.com/tmux-plugins/tpm ~/.config/tmux/plugins/tpm

echo "Done! Notes:"
echo " - Run 'PlugInstall' from vim to setup plugins"
