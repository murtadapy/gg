import argparse
from typing import Callable

from gg.commands import InitiateCommand
from gg.commands import StatusCommand
from gg.commands import SprintCommand
from gg.commands import CommitCommand
from gg.commands import ConfigCommand
from gg.file_manager import FileManager
from gg.blob_manager import BlobManager
from gg.database import Database
from gg.logger import Logger


class GG:
    def __init__(self) -> None:
        self.database = Database()
        self.file_manager = FileManager()
        self.blob_manager = BlobManager(self.file_manager, self.database)
        self.logger = Logger()

    def _init(self, _: argparse.Namespace) -> None:
        InitiateCommand(self.database,
                        self.file_manager,
                        self.blob_manager,
                        self.logger).execute()

    def _status(self, _: argparse.Namespace) -> None:
        StatusCommand(self.database,
                      self.file_manager,
                      self.blob_manager,
                      self.logger).execute()

    def _commit(self, args: argparse.Namespace) -> None:
        CommitCommand(self.database,
                      self.file_manager,
                      self.blob_manager,
                      self.logger).execute()

    def _sprint(self, args: argparse.Namespace) -> None:
        SprintCommand(self.database,
                      self.file_manager,
                      self.blob_manager,
                      self.logger,
                      args.n).execute()

    def _config(self, args: argparse.Namespace) -> None:
        ConfigCommand(self.database,
                      self.file_manager,
                      self.blob_manager,
                      self.logger,
                      args.key,
                      args.value).execute()

    def _run_command(self, args: argparse.Namespace) -> None:
        commands: dict[str, Callable[[argparse.Namespace], None]] = {
            "init": self._init,
            "status": self._status,
            "sprint": self._sprint,
            "commit": self._commit,
            "config": self._config,
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

        commit = subparsers.add_parser("commit", help="Commit changes")
        self.add_generic_arguments(commit)

        sprint = subparsers.add_parser("sprint", help="Create a new sprint")
        sprint.add_argument("-n",
                            help="Sprint name",
                            required=True)
        self.add_generic_arguments(sprint)

        config = subparsers.add_parser("config", help="Change Config Values")
        config.add_argument("--key",
                            help="Config Key",
                            required=True)

        config.add_argument("--value",
                            help="Config Value",
                            required=True)
        self.add_generic_arguments(config)

        args = parser.parse_args()
        self._setup_logger(args)
        self._run_command(args)

    def run(self) -> None:
        self.parse()
