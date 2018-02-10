#!/usr/bin/python3
from os import chdir, path, listdir, makedirs, unlink, walk
from os.path import join as j
from subprocess import check_output
from sys import argv
from time import sleep
from shutil import rmtree, copy2
from tempfile import mkdtemp
from yaml import load

def read_config(fname):
    with open(fname, 'r') as config_f:
        return load(config_f)

def raw_git(repo_dir, args):
    return check_output(
        'git ' + args,
        cwd=repo_dir,
        encoding='utf-8',
        shell=True
    ).strip().split('\n')

def setup_git():
    origin_url = raw_git('.', 'remote get-url origin')[0]
    repo_dir = mkdtemp()
    wrapped_git = lambda args: raw_git(repo_dir, args)
    wrapped_git('clone "%s" .' % origin_url)
    return (wrapped_git, repo_dir)

def get_parts(item, hostname):
    parts = list(item['all']) if 'all' in item else []
    parts += item[hostname] if hostname in item else []
    return parts

def create_host_branch(git, repo_dir, hostname):
    branches = [x.lstrip('* ') for x in git('branch -a')]

    # Create empty branch if necessary
    if 'remotes/origin/' + hostname not in branches:
        git('checkout --orphan "%s"' % hostname)
        git('reset -- *')
    else:
        git('checkout --track "origin/%s"' % hostname)

    # Remove everything - it will all be recreated
    for item in listdir(repo_dir):
        abs_path = j(repo_dir, item)
        if item == '.git':
            continue
        if path.isdir(abs_path):
            rmtree(abs_path)
        else:
            unlink(abs_path)

def assemble_host(git, repo_dir, host, files, folders):
    hostname = host['name']

    print('Assembling', hostname)

    create_host_branch(git, repo_dir, hostname)

    # Copy the folders
    folder_files = []
    for folder in folders:
        print('\t', folder['path'])

        # Has to be done manually because we need to add files
        # to the gitignore
        for part in get_parts(folder, hostname):
            for cwd, _, w_files in walk(part):
                for file in w_files:
                    src_path = j(cwd, file)
                    print('\t\t', src_path)
                    dest_dir = j(repo_dir, folder['path'], path.relpath(cwd, part))
                    makedirs(dest_dir, exist_ok=True)
                    copy2(src_path, j(dest_dir, file))
                    folder_files.append({
                        'path': j(path.relpath(dest_dir, repo_dir), file)
                    })

    # Compile the files
    for file in files:
        print('\t', file['path'])

        # Set up the assembled file
        makedirs(j(repo_dir, path.dirname(file['path'])), exist_ok=True)

        with open(j(repo_dir, file['path']), 'wb') as assy_f:

            # Build the file
            for part in get_parts(file, hostname):
                print('\t\t', part)
                try:
                    with open(part, 'rb') as part_f:
                        assy_f.write(part_f.read())
                    assy_f.write(b'\n')
                except:
                    print('Failed to open/read', part)

    # Build the gitignore file
    with open(j(repo_dir, '.gitignore'), 'w') as ignore_f:
        ignore_f.write('*\n!.gitignore\n')
        for file in files + folder_files:
            ignore_f.write('!%s\n' % file['path'])

    # Create a commit
    git('add -A')
    try:
        git('commit -m "Updated with DotCom"')
    except:
        print('NOTICE: No changes on host', hostname)
    git('checkout master')

def main():
    if len(argv) < 2:
        print('Usage: {} build_yaml'.format(argv[0]))
        exit(1)

    config = read_config(argv[1])

    git, repo_dir = setup_git()

    # Chroot
    chdir(path.dirname(argv[1]) or '.')

    for host in config['hosts']:
        assemble_host(git, repo_dir, host, config['files'], config['folders'])

    print('Repo updated in', repo_dir)
    save = input('Do you want to push the changes? y/[n]')

    if save.lower() == 'y':
        print('Pushing')
        git('push --all -u')

    print('Deleting temporary repo')
    rmtree(repo_dir)

    print('Done!')

if __name__ == '__main__':
    main()
