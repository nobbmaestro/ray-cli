import argparse
import sys

from .__version__ import __version__

APP_NAME = "ray-cli"
DESCRIPTION = "Command line utility for generating and broadcast DMX over sACN."


def parse_args():
    argparser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=DESCRIPTION,
        add_help=False,
    )

    query_group = argparser.add_argument_group("query options")
    query_group.add_argument(
        "-h",
        "--help",
        action="help",
        help="print help and exit",
    )
    query_group.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {__version__}",
    )

    args = argparser.parse_args()

    return args


def shell(args):  # pylint: disable=unused-argument
    pass


def main():
    try:
        args = parse_args()
        shell(args)

    except KeyboardInterrupt:
        print("\nCancelling...")
        sys.exit(1)

    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Failed with error: {exc}")
        sys.exit(1)

    else:
        sys.exit(0)
