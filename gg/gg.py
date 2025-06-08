import argparse
from typing import Callable

from gg.commands import InitiateCommand


def _init(args: argparse.Namespace) -> None:
    InitiateCommand().execute()


def _map_command(args: argparse.Namespace) -> None:
    commands: dict[str, Callable[[argparse.Namespace], None]] = {
        "init": _init
    }
    commands[args.command](args)


def parse() -> None:
    parser = argparse.ArgumentParser(description="GG: Good to Git")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser('init', help="Initiate gg repostiroy")

    args = parser.parse_args()
    _map_command(args)


def run() -> None:
    parse()
