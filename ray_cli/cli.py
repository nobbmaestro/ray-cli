import argparse
import ipaddress
import sys

from ray_cli.dispatchers import SACNDispatcher
from ray_cli.modes import (
    ChaseModeOutputGenerator,
    Mode,
    RampDownModeOutputGenerator,
    RampModeOutputGenerator,
    RampUpModeOutputGenerator,
    SquareModeOutputGenerator,
    StaticModeOutputGenerator,
)
from ray_cli.utils import Feedback, generate_settings_report

from .__version__ import __version__
from .app import App

APP_NAME = "ray-cli"
DESCRIPTION = "Command line utility for generating and broadcast DMX over sACN."
MAX_CHANNELS = 512
MAX_INTENSITY = 255


def print_greetings(args):
    title = "Ray CLI"
    body = generate_settings_report(
        args=args,
        max_channels=MAX_CHANNELS,
        max_intensity=MAX_INTENSITY,
    )

    greetings = f"\n{title}\n\n{body}\n"

    print(greetings)


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
            raise argparse.ArgumentTypeError(f"Value mest be between {lower} and {upper}")
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
        default="ramp",
        choices=[mode.value for mode in Mode],  # type: ignore
        help="broadcast mode, defaults to ramp",
    )
    argparser.add_argument(
        "-d",
        "--duration",
        default=None,
        type=float,
        help="broadcast duration in seconds, defaults to INDEFINITE",
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
    argparser.add_argument(
        "--dst",
        type=ipaddress.IPv4Address,
        default=None,
        help="IP address of the dmx destination, defaults to MULTICAST",
    )

    display_group = argparser.add_argument_group("display options")
    display_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="run in verbose mode",
    )
    display_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="run in quiet mode",
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

        if args.quiet:
            feedback = Feedback.NONE
        elif args.verbose:
            feedback = Feedback.TABULAR
        else:
            feedback = Feedback.PROGRESS_BAR

        mode_to_generator = {
            Mode.CHASE: ChaseModeOutputGenerator,
            Mode.RAMP: RampModeOutputGenerator,
            Mode.RAMP_DOWN: RampDownModeOutputGenerator,
            Mode.RAMP_UP: RampUpModeOutputGenerator,
            Mode.SQUARE: SquareModeOutputGenerator,
            Mode.STATIC: StaticModeOutputGenerator,
        }

        generator_class = mode_to_generator.get(args.mode)
        if generator_class is None:
            raise NotImplementedError(f"Generator '{args.mode}' does not exist.")

        generator = generator_class(
            channels=args.channels,
            fps=args.fps,
            frequency=args.frequency,
            intensity=args.intensity,
        )

        dispatcher = SACNDispatcher(
            channels=args.channels,
            fps=args.fps,
            universes=args.universes,
            src_ip_address=args.IP_ADDRESS,
            dst_ip_address=args.dst,
        )

        if not args.quiet:
            print_greetings(args)

        app = App(
            generator=generator,
            dispatcher=dispatcher,
            channels=args.channels,
            fps=args.fps,
            duration=args.duration,
        )

        app.run(feedback)

        if not args.quiet:
            print("\nDone!")

    except KeyboardInterrupt:
        print("\nCancelling...")
        sys.exit(1)

    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Failed with error: {exc}")
        sys.exit(1)

    else:
        sys.exit(0)
