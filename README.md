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

List entries (default user `known_hosts`):

```bash
scrub_ssh list
```

List HTB-suspect entries only (using config presets):

```bash
scrub_ssh list --htb
```

Delete all HTB-suspect entries, but **dry-run** first:

```bash
scrub_ssh delete --htb --dry-run
scrub_ssh delete --htb
```

Delete everything for an HTB VPN / VIP subnet:

```bash
scrub_ssh delete --cidr 10.10.10.0/24 --dry-run
scrub_ssh delete --cidr 10.10.10.0/24
```

Delete entries for a single box IP:

```bash
scrub_ssh delete --ip 10.10.10.10
```

Delete entries matching a hostname pattern:

```bash
scrub_ssh delete --match "*htb*"
```

Interactive cleanup of a specific file:

```bash
scrub_ssh interactive --file ~/.ssh/known_hosts
```

Target system-wide `known_hosts` (needs sudo):

```bash
sudo scrub_ssh list --system
sudo scrub_ssh delete --system --htb --dry-run
sudo scrub_ssh delete --system --htb
```

Create just a backup of your `known_hosts`:

```bash
scrub_ssh backup
```

Restore from a backup:

```bash
scrub_ssh restore ~/.ssh/known_hosts.bak-20260316-145230
```

For all options:

```bash
scrub_ssh --help
scrub_ssh list --help
scrub_ssh delete --help
```


