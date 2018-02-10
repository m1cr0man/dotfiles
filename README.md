# M1cr0man's Dotfiles

Configs for all my Linux-based devices

## Usage

Branches are generated for each device using `dotcom.py`
(see [Compiling](#compiling)), thus the only client requirement is `git`.
Clone a branch into your home directory.

```bash
git clone -b $(hostname) https://github.com/m1cr0man/dotfiles.git ~/
```

## Compiling

#### Requirements

- Python 3
- PyYAML

```bash
./dotcom.py configs/dotfiles.yaml
```

When prompted, enter 'y' to update remote branches for each device

## Making Changes

For modifications it is only necessary to edit the file and re-compile the
branches. If you are adding or removing a file you may need to update
`dotfiles.yaml` depending on where you put it.

## Adding Device-specific Configs

Dotcom is capable of merging multiple files into one depending on the name of
the branch it is working on. See the i3/sway config setup in `dotfiles.yaml`
for a complete example.
