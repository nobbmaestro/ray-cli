import argparse
import ipaddress
import sys

from ray_cli.modes import Mode, StaticModeOutputGenerator
from ray_cli.sacn import SACNDispatcher

from .__version__ import __version__

APP_NAME = "ray-cli"
DESCRIPTION = "Command line utility for generating and broadcast DMX over sACN."
MAX_CHANNELS = 512
MAX_INTENSITY = 255


def range_limited_int_type(
    upper: int,
    lower: int = 0,
):
    def validate(arg: int) -> int:
        try:
            value = int(arg)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"Invalid integer value: '{arg}'") from exc
        if value < lower or value > upper:
            raise argparse.ArgumentTypeError(
                f"Value mest be between {lower} and {upper}"
            )
        return value

    return validate


def parse_args():
    argparser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=DESCRIPTION,
        add_help=False,
    )

    argparser.add_argument(
        "IP_ADDRESS",
        type=ipaddress.IPv4Address,
        help="IP address of the dmx source",
    )
    argparser.add_argument(
        "-m",
        "--mode",
        type=Mode,
        default="static",
        choices=[mode.value for mode in Mode],  # type: ignore
        help="broadcast mode, defaults to ramp",
    )
    argparser.add_argument(
        "-u",
        "--universes",
        default=(1,),
        nargs="+",
        type=int,
        help="sACN universe(s) to send to",
    )
    argparser.add_argument(
        "-c",
        "--channels",
        default=24,
        type=range_limited_int_type(
            lower=0,
            upper=MAX_CHANNELS,
        ),  # type: ignore
        help=f"DMX channels at universe to send to, (0, ...{MAX_CHANNELS})",
    )
    argparser.add_argument(
        "-i",
        "--intensity",
        default=10,
        type=range_limited_int_type(
            lower=0,
            upper=MAX_INTENSITY,
        ),  # type: ignore
        help=f"DMX channels output intensity, (0, ...{MAX_INTENSITY})",
    )
    argparser.add_argument(
        "-f",
        "--frequency",
        default=1.0,
        type=float,
        help="signal frequency",
    )
    argparser.add_argument(
        "--fps",
        default=10,
        type=int,
        help="frames per second per universe",
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


def main():
    try:
        args = parse_args()

        generator = StaticModeOutputGenerator(
            channels=args.channels,
            fps=args.fps,
            frequency=args.frequency,
            intensity=args.intensity,
        )

        dispatcher = SACNDispatcher(
            generator=generator,
            channels=args.channels,
            fps=args.fps,
            universes=args.universes,
            src_ip_address=args.IP_ADDRESS,
        )
        dispatcher.run()

    except KeyboardInterrupt:
        print("\nCancelling...")
        sys.exit(1)

    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Failed with error: {exc}")
        sys.exit(1)

    else:
        sys.exit(0)
