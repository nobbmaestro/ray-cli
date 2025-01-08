def generate_settings_report(
    args,
    max_channels,
    max_intensity,
    padding=12,
) -> str:
    row_template = "{desc:>{padding}s}: {value:.<26s}{info:.<12s}"
    report_template = (
        "{src}\n{dst}\n\n{mod}\n{dur}\n{frq}\n{fps}\n\n{uni}\n{chn}\n{ity}\n"
    )

    return report_template.format(
        src=row_template.format(
            desc="source",
            value=str(args.IP_ADDRESS),
            padding=padding,
            info="",
        ),
        dst=row_template.format(
            desc="destination",
            value=(str(args.dst) if args.dst else "MULTICAST"),
            padding=padding,
            info="",
        ),
        mod=row_template.format(
            desc="mode",
            value=args.mode.value.upper(),
            padding=padding,
            info="",
        ),
        dur=row_template.format(
            desc="duration",
            value=f"{args.duration:.2f} s" if args.duration else "INDEFINITE",
            info="",
            padding=padding,
        ),
        frq=row_template.format(
            desc="frequency",
            value=f"{args.frequency:.2f} Hz",
            info="",
            padding=padding,
        ),
        fps=row_template.format(
            desc="resolution",
            value=f"{args.fps} fps",
            info="",
            padding=padding,
        ),
        uni=row_template.format(
            desc="universes",
            value=", ".join(map(str, args.universes)),
            info="(out of 1-8)",
            padding=padding,
        ),
        chn=row_template.format(
            desc="channels",
            value=str(args.channels),
            info=f"(out of {max_channels})",
            padding=padding,
        ),
        ity=row_template.format(
            desc="intensity",
            value=f"{str(args.intensity_min)} - {str(args.intensity)}",
            info=f"(out of {max_intensity})",
            padding=padding,
        ),
    )
