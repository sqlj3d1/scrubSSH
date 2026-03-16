scrubssh
========

`scrubssh` is a Python CLI tool for inspecting, filtering, and cleaning SSH `known_hosts` files, with features tailored for HackTheBox players who frequently rotate targets.

## Features

- List, filter, and delete entries from user (`~/.ssh/known_hosts`) and system-wide (`/etc/ssh/ssh_known_hosts`) files.
- Safe-by-default: automatic timestamped backups before any write.
- Powerful filters: host, IP, CIDR ranges, glob/regex, line numbers.
- HTB-focused presets via `--htb` (patterns and ranges from a config file).
- Interactive mode for reviewing and selecting entries before deletion.
- Non-interactive subcommands for scripting in your workflows.

## Basic Usage

- List entries (default user `known_hosts`):

```bash
scrub_ssh list
```

- Dry-run delete of HTB-related entries:

```bash
scrub_ssh delete --htb --dry-run
```

- Interactive cleanup of a specific file:

```bash
scrub_ssh interactive --file ~/.ssh/known_hosts
```

More detailed usage and examples will be available via `scrub_ssh --help` once the tool is installed.

