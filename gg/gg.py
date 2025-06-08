import os
import sys
import argparse
from typing import Callable

from gg.commands import InitiateCommand
from gg.commands import StatusCommand
from gg.logger import Logger


PATH = os.path.join(sys.path[0], ".gg")
LOGGER = Logger()


def _init(_: argparse.Namespace) -> None:
    InitiateCommand(PATH, LOGGER).execute()


def _status(_: argparse.Namespace) -> None:
    StatusCommand(PATH, LOGGER).execute()


def _run_command(args: argparse.Namespace) -> None:
    commands: dict[str, Callable[[argparse.Namespace], None]] = {
        "init": _init,
        "status": _status,
    }

    commands[args.command](args)


def _setup_logger(args: argparse.Namespace) -> None:
    if args.q:
        LOGGER.suppress()

    if args.v:
        LOGGER.verbose()


def add_generic_arguments(suparser: argparse.ArgumentParser) -> None:
    suparser.add_argument("-q",
                          default=False,
                          help="Suppress Logging",
                          action="store_true")

    suparser.add_argument("-v",
                          default=False,
                          help="Verbose Logging",
                          action="store_true")


def parse() -> None:
    parser = argparse.ArgumentParser(description="GG: Good to Git")

    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Initiate gg repostiroy")
    add_generic_arguments(init)

    status = subparsers.add_parser("status", help="Status of repostiroy")
    add_generic_arguments(status)

    args = parser.parse_args()
    _setup_logger(args)
    _run_command(args)


def run() -> None:
    parse()
