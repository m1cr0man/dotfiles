# DotCom - Dotfile Compiler
# 2017 m1cr0man

from os import path
from glob import iglob
from subprocess import call
from json import load

def concatenate(source_globs, output_file):
    with open(output_file, 'w') as output:
        for source_glob in source_globs:
            for config in iglob(source_glob):
                with open(config, 'r') as config_data:
                    output.write('\n#%s\n' % path.basename(config).capitalize())
                    output.write(config_data.read())

def gethostname():
    with open('/etc/hostname', 'r') as hostname_file:
        return hostname_file.read().strip()

def main():
    # Determine what computer we're on
    hostname = gethostname()

    # Load the config source data
    configs = {}

    with open('dotcom.json', 'r') as raw_configs:
        configs = load(raw_configs)

    # Compile all the configs
    for (config, contents) in configs.items():
        source_globs = contents.configs
        source_globs += contents.hosts[hostname]
        concatenate(source_globs, config)
        call(contents.reload_command)

main()
