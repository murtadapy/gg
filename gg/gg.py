import os
import sys
import argparse
from typing import Callable

from gg.commands import InitiateCommand
from gg.commands import StatusCommand
from gg.database import Database
from gg.logger import Logger


class GG:
    def __init__(self) -> None:
        self.path = os.path.join(sys.path[0], ".gg")
        self.database = Database(self.path)
        self.logger = Logger()

    def _init(self, _: argparse.Namespace) -> None:
        InitiateCommand(self.path, self.database, self.logger).execute()

    def _status(self, _: argparse.Namespace) -> None:
        StatusCommand(self.path, self.database, self.logger).execute()

    def _run_command(self, args: argparse.Namespace) -> None:
        commands: dict[str, Callable[[argparse.Namespace], None]] = {
            "init": self._init,
            "status": self._status,
        }

        commands[args.command](args)

    def _setup_logger(self, args: argparse.Namespace) -> None:
        if args.q:
            self.logger.suppress()

        if args.v:
            self.logger.verbose()

    def add_generic_arguments(self, suparser: argparse.ArgumentParser) -> None:
        suparser.add_argument("-q",
                              default=False,
                              help="Suppress Logging",
                              action="store_true")

        suparser.add_argument("-v",
                              default=False,
                              help="Verbose Logging",
                              action="store_true")

    def parse(self) -> None:
        parser = argparse.ArgumentParser(description="GG: Good to Git")

        subparsers = parser.add_subparsers(dest="command", required=True)

        init = subparsers.add_parser("init", help="Initiate gg repostiroy")
        self.add_generic_arguments(init)

        status = subparsers.add_parser("status", help="Status of repostiroy")
        self.add_generic_arguments(status)

        args = parser.parse_args()
        self._setup_logger(args)
        self._run_command(args)

    def run(self) -> None:
        self.parse()
