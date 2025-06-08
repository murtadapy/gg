import argparse


def parse() -> None:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser('init', help="Initiate gg repostiroy")

    parser.parse_args()


def run() -> None:
    parse()
