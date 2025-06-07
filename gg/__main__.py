import argparse

from ppaste.commands import Install


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--install",
                        action="store_true",
                        help="Run the installation process")
    args = parser.parse_args()

    if args.install:
        Install.execute()


if __name__ == "__main__":
    raise SystemExit(main())
