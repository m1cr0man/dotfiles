call plug#begin('~/.config/nvim/plugged')

Plug 'terryma/vim-multiple-cursors'
Plug 'airblade/vim-gitgutter'
Plug 'ntpeters/vim-better-whitespace'
Plug 'harish2704/MatchTag'
Plug 'junegunn/rainbow_parentheses.vim'

call plug#end()

filetype plugin indent on

set clipboard+=unnamedplus

" Top statusline disabled because I'm using tmux
set laststatus=0

set undofile
set ruler
set number
set tabstop=4
set shiftwidth=4
set autoindent

"From https://github.com/neovim/neovim/blob/master/runtime/vimrc_example.vim
augroup vimrcEx
  autocmd!

  " For all text files set 'textwidth' to 78 characters.
  autocmd FileType text setlocal textwidth=78

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") |
    \   execute "normal! g`\"" |
    \ endif

augroup END

" Convenient command to see the difference between the current buffer and the
" file it was loaded from, thus the changes you made.
" Only define it when not defined already.
if !exists(":DiffOrig")
  command DiffOrig vert new | set buftype=nofile | read ++edit # | 0d_ | diffthis
                 \ | wincmd p | diffthis
endif

set termguicolors
set background=dark
colorscheme m1cr0man

function Spacetab(size)
	execute "set tabstop=".a:size
	execute "set shiftwidth=".a:size
	set expandtab
	retab
end

let g:rainbow#pairs = [['(', ')'], ['[', ']'], ['{', '}'], ['<', '>']]
autocmd FileType * RainbowParenthesesfunction
