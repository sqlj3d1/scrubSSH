import argparse
import sys
from pathlib import Path

from . import __version__
from . import config as config_mod
from . import ops


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scrub_ssh",
        description="Inspect, filter, and clean SSH known_hosts files (optimized for HackTheBox workflows).",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        metavar="PATH",
        help="Path to known_hosts file (default: user known_hosts).",
    )

    parser.add_argument(
        "--system",
        action="store_true",
        help="Use system-wide known_hosts (usually /etc/ssh/ssh_known_hosts).",
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Minimal output.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    list_p = subparsers.add_parser("list", help="List entries with optional filters.")
    add_common_filters(list_p)
    list_p.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format for scripting.",
    )

    # delete
    delete_p = subparsers.add_parser("delete", help="Delete entries matching filters.")
    add_common_filters(delete_p)
    delete_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without modifying files.",
    )

    # backup
    backup_p = subparsers.add_parser("backup", help="Create a backup of the target known_hosts file.")
    backup_p.set_defaults(command="backup")

    # restore
    restore_p = subparsers.add_parser("restore", help="Restore a known_hosts file from a backup.")
    restore_p.add_argument("backup_path", metavar="BACKUP_PATH", help="Path to backup file to restore from.")

    # interactive
    interactive_p = subparsers.add_parser(
        "interactive",
        help="Interactive TUI-like mode for inspecting and selecting entries to delete.",
    )
    add_common_filters(interactive_p)

    return parser


def add_common_filters(p: argparse.ArgumentParser) -> None:
    p.add_argument("--host", metavar="HOST", help="Match by hostname.")
    p.add_argument("--ip", metavar="IP", help="Match by IP address.")
    p.add_argument(
        "--match",
        metavar="PATTERN",
        help="Glob-like pattern for hosts (e.g. '*htb*', '10.10.*.*').",
    )
    p.add_argument(
        "--regex",
        metavar="REGEX",
        help="Regular expression applied to the raw line.",
    )
    p.add_argument(
        "--cidr",
        metavar="CIDR",
        help="CIDR range for IPs (e.g. 10.10.10.0/24).",
    )
    p.add_argument(
        "--line",
        type=int,
        metavar="N",
        help="Match a specific line number (1-based).",
    )
    p.add_argument(
        "--lines",
        metavar="RANGE",
        help="Match a line range, e.g. '10-20'.",
    )
    p.add_argument(
        "--htb",
        action="store_true",
        help="Apply HackTheBox-related presets from config (IP ranges / host patterns).",
    )
    p.add_argument(
        "--or",
        dest="use_or",
        action="store_true",
        help="Combine filters using logical OR instead of AND.",
    )


def resolve_file(args: argparse.Namespace, cfg: config_mod.Config) -> Path:
    if args.system:
        return config_mod.DEFAULT_SYSTEM_KNOWN_HOSTS
    if args.file:
        return Path(args.file).expanduser()
    if cfg.default_known_hosts_path:
        return Path(cfg.default_known_hosts_path).expanduser()
    return config_mod.DEFAULT_USER_KNOWN_HOSTS


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    cfg = config_mod.load_config()
    target_file = resolve_file(args, cfg)

    verbosity = 0
    if args.quiet:
        verbosity = -1
    else:
        verbosity = args.verbose

    if args.command == "list":
        return ops.cmd_list(target_file, args, cfg, verbosity)
    if args.command == "delete":
        return ops.cmd_delete(target_file, args, cfg, verbosity)
    if args.command == "backup":
        return ops.cmd_backup(target_file, verbosity)
    if args.command == "restore":
        return ops.cmd_restore(target_file, Path(args.backup_path), verbosity)
    if args.command == "interactive":
        return ops.cmd_interactive(target_file, args, cfg, verbosity)

    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

