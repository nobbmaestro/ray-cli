import argparse
import importlib.metadata
import ipaddress
import sys
from typing import Callable

from ray_cli.core.sender_pool import SenderPool
from ray_cli.modes import Mode, build_generator
from ray_cli.transports.sacn.sender import SACNSender
from ray_cli.utils import CustomHelpFormatter, Feedback, generate_settings_report

from .__version__ import __version__
from .app import App

PACKAGE_NAME = importlib.metadata.metadata("ray-cli")["Name"]
PACKAGE_SUMMARY = importlib.metadata.metadata("ray-cli")["Summary"]

MAX_CHANNELS = 512
MAX_FPS = 10**4
MAX_PACKETS = 10**9
MIN_INTENSITY = 0
MAX_INTENSITY = 255
MIN_PRIORITY = 0
MAX_PRIORITY = 200
MAX_UNIVERSE = 63999
MAX_WORKERS = 100


def print_report(args):
    title = f"{PACKAGE_NAME} {__version__}"
    body = generate_settings_report(
        args=args,
        max_channels=MAX_CHANNELS,
        max_priority=MAX_PRIORITY,
        max_intensity=MAX_INTENSITY,
        max_workers=MAX_WORKERS,
    )
    print(f"\n{title}\n\n{body}\n")


def range_limited_int_type(
    upper: int,
    lower: int = 1,
) -> Callable:
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


def non_zero_float_type() -> Callable:
    def validate(arg: float) -> float:
        try:
            value = float(arg)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"Invalid float value: '{arg}'") from exc
        if value <= 0.0:
            raise argparse.ArgumentTypeError("Value must be non-zero")
        return value

    return validate


def parse_args(args=None):
    argparser = argparse.ArgumentParser(
        prog=PACKAGE_NAME,
        description=PACKAGE_SUMMARY,
        add_help=False,
        formatter_class=CustomHelpFormatter,
    )

    argparser.add_argument(
        "IP_ADDRESS",
        nargs="?",
        type=ipaddress.IPv4Address,
        default=ipaddress.IPv4Address("0.0.0.0"),
        help="IP address of the DMX source (default: %(default)s)",
    )
    argparser.add_argument(
        "-m",
        "--mode",
        type=Mode,
        default=Mode.RAMP,
        choices=list(Mode),
        help="DMX signal shape mode (default: %(default)s)",
    )
    argparser.add_argument(
        "-u",
        "--universes",
        default=(1,),
        nargs="+",
        type=range_limited_int_type(upper=MAX_UNIVERSE),
        help=f"sACN universe(s) to send to (range: 1-{MAX_UNIVERSE}, default: 1)",
    )
    argparser.add_argument(
        "-c",
        "--channels",
        default=24,
        type=range_limited_int_type(upper=MAX_CHANNELS),
        help=f"DMX channels at universe to send to (range: 1-{MAX_CHANNELS}, default: %(default)s)",  # noqa: E501 # pylint: disable=line-too-long
    )
    argparser.add_argument(
        "-i",
        "--intensity",
        default=10,
        type=range_limited_int_type(upper=MAX_INTENSITY),
        help=f"DMX channels output intensity (range: 1-{MAX_INTENSITY}, default: %(default)s)",  # noqa: E501 # pylint: disable=line-too-long
    )
    argparser.add_argument(
        "-I",
        "--intensity-min",
        default=0,
        type=range_limited_int_type(lower=MIN_INTENSITY, upper=MAX_INTENSITY),
        help=f"DMX channels minimum output intensity (range: {MIN_INTENSITY}-{MAX_INTENSITY}, default: 0)",  # noqa: E501 # pylint: disable=line-too-long
    )
    argparser.add_argument(
        "-p",
        "--priority",
        default=100,
        type=range_limited_int_type(lower=MIN_PRIORITY, upper=MAX_PRIORITY),
        help=f"DMX source priority (range: {MIN_PRIORITY}-{MAX_PRIORITY}, default: %(default)s)",  # noqa: E501 # pylint: disable=line-too-long
    )
    argparser.add_argument(
        "-f",
        "--frequency",
        default=1.0,
        type=non_zero_float_type(),
        help="frequency of the generated signal (default: %(default)s)",
    )
    argparser.add_argument(
        "--dst",
        type=ipaddress.IPv4Address,
        default=None,
        help="IP address of the DMX destination (default: MULTICAST)",
    )

    runtime_group = argparser.add_argument_group("runtime options")
    runtime_group.add_argument(
        "-w",
        "--workers",
        default=1,
        type=range_limited_int_type(upper=MAX_WORKERS),
        help="number of sender workers per universe (default: %(default)s)",
    )
    runtime_exclusive_group = runtime_group.add_mutually_exclusive_group()
    runtime_exclusive_group.add_argument(
        "-P",
        "--packets",
        default=None,
        type=range_limited_int_type(upper=MAX_PACKETS),
        help="number of packets to send per universe per worker (default: INDEFINITE)",
    )
    runtime_exclusive_group.add_argument(
        "-d",
        "--duration",
        default=None,
        type=non_zero_float_type(),
        help="broadcast duration in seconds (default: INDEFINITE)",
    )
    runtime_group.add_argument(
        "--fps",
        default=10,
        type=range_limited_int_type(upper=MAX_FPS),
        help="frames per second per universe (default: %(default)s)",
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

    operational_group = argparser.add_argument_group("operational options")
    operational_group.add_argument(
        "--dry",
        action="store_true",
        help="simulate outputs without broadcast",
    )
    operational_group.add_argument(
        "--purge",
        action="store_true",
        help="send zero-data on all channels and exit",
    )

    query_group = argparser.add_argument_group("query options")
    query_group.add_argument(
        "-h",
        "--help",
        action="help",
        help="print help and exit",
    )
    query_group.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return argparser.parse_args(args)


def main(args=None):
    try:
        args = parse_args(args)

        if args.quiet:
            feedback = None
        elif args.verbose or args.dry:
            feedback = Feedback.TABULAR
        else:
            feedback = Feedback.PROGRESS_BAR

        generator = build_generator(
            mode=args.mode,
            channels=args.channels,
            fps=args.fps,
            frequency=args.frequency,
            intensity_upper=args.intensity,
            intensity_lower=args.intensity_min,
        )

        sender_pool = SenderPool(
            senders=[
                SACNSender(
                    source_name=(
                        f"{PACKAGE_NAME} {__version__}"
                        + (f" [worker:{i}]" if args.workers > 1 else "")
                    ),
                    universes=args.universes,
                    priority=args.priority,
                    src=args.IP_ADDRESS,
                    dst=args.dst,
                )
                for i in range(args.workers)
            ]
        )

        if not args.quiet and not args.purge:
            print_report(args)

        app = App(
            generator=generator,
            sender=sender_pool,
            channels=args.channels,
            fps=args.fps,
            max_packets=(
                args.packets
                if args.packets is not None
                else args.fps * args.duration if args.duration else None
            ),
        )

        if args.purge:
            app.purge_output()
        else:
            app.run(feedback, args.dry)

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
