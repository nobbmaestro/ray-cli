import ipaddress
from typing import Optional, Union

import pytest

from ray_cli.cli import parse_args
from ray_cli.modes import Mode


def helper_parse_args(
    arg: Optional[str] = None,
    value: Optional[Union[str, list]] = None,
    positional_args: str = "1.1.1.1",
):
    args = [positional_args] if positional_args else []

    if arg is not None:
        args.append(arg)

    if isinstance(value, list):
        args.extend(value)

    elif value is not None:
        args.append(value)

    return parse_args(args)


@pytest.mark.parametrize("value, expected", [
    ("1.1.1.1", ipaddress.ip_address("1.1.1.1")),
    ("192.168.5.1", ipaddress.ip_address("192.168.5.1")),
])  # fmt: skip
def test_parse_args_ip_address_valid(value, expected):
    parsed = helper_parse_args(positional_args=value)
    assert parsed.IP_ADDRESS == expected


@pytest.mark.parametrize("value", [
    "",
    "1",
    "1.1.1",
    "192.168.1.1000",
    "192.168.1.a",
    "a.a.a.a",
])  # fmt: skip
def test_parse_args_ip_address_invalid(value):
    with pytest.raises(SystemExit):
        helper_parse_args(positional_args=value)


@pytest.mark.parametrize("value, expected", [
    (mode.value, mode) for mode in Mode
])  # fmt: skip # type: ignore
@pytest.mark.parametrize("arg", [
    "-m",
    "--mode",
])  # fmt: skip
def test_parse_args_mode_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.mode == expected


@pytest.mark.parametrize("value", [
    "",
    "typo",
    "1",
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-m",
    "--mode",
])  # fmt: skip
def test_parse_args_mode_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)


@pytest.mark.parametrize("value, expected", [
    ("1", 1.0),
    ("1.0", 1.0),
    ("1.5", 1.5),
    ("0.00001", 0.00001),
    ("1000000", 1000000),
],)  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-d",
    "--duration",
])  # fmt: skip
def test_parse_args_duration_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.duration == expected


@pytest.mark.parametrize("value", [
    "",
    "0",
    "0.0",
    "-1",
    "-1.0",
    "not a float",
],)  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-d",
    "--duration",
])  # fmt: skip
def test_parse_args_duration_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)


@pytest.mark.parametrize("value, expected", [
    ("1", [1]),
    ("4", [4]),
    (["1", "4"], [1, 4]),
    (["1", "2", "3", "4", "5", "6", "7", "8"], [1, 2, 3, 4, 5, 6, 7, 8]),
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-u",
    "--universes",
])  # fmt: skip
def test_parse_args_universes_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.universes == expected


@pytest.mark.parametrize("value", [
    "",
    "0",
    "-1",
    "9",
    "a",
    ["1", "0"],
    ["0", "9"],
    ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    ["0", "1", "2", "3", "4", "5", "6", "7", "8"],
    ["1", "2", "3", "4", "5", "6", "7", "8", "a"],
    ["1", "2", "3", "4", "5", "6", "7", "8", "-1"],
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-u",
    "--universes",
])  # fmt: skip
def test_parse_args_universes_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)


@pytest.mark.parametrize("value, expected", [
    ("1", 1),
    ("100", 100),
    ("512", 512),
],)  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-c",
    "--channels",
])  # fmt: skip
def test_parse_args_channels_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.channels == expected


@pytest.mark.parametrize("value", [
    "",
    "0",
    "513",
    "1.0",
    "512.0",
    "-1",
    "-1.0",
    "-512.0",
    "not an int",
],)  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-c",
    "--channels",
])  # fmt: skip
def test_parse_args_channels_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)


@pytest.mark.parametrize("value, expected", [
    ("1", 1),
    ("2", 2),
    ("10", 10),
    ("100", 100),
    ("255", 255),
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-i",
    "--intensity",
])  # fmt: skip
def test_parse_args_intensity_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.intensity == expected


@pytest.mark.parametrize("value", [
    "",
    "0",
    "256",
    "1.0",
    "255.0",
    "-1",
    "-1.0",
    "-255.0",
    "not an int",
],)  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-i",
    "--intensity",
])  # fmt: skip
def test_parse_args_intensity_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)


@pytest.mark.parametrize("value, expected", [
    ("1", 1),
    ("2", 2),
    ("10", 10),
    ("100", 100),
    ("1000", 1000),
    ("10000", 10000),
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "--fps",
])  # fmt: skip
def test_parse_args_fps_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.fps == expected


@pytest.mark.parametrize("value", [
    "",
    "0",
    "10001",
    "1.0",
    "10000.0",
    "-1",
    "-1.0",
    "-10000.0",
    "not an int",
],)  # fmt: skip
@pytest.mark.parametrize("arg", [
    "--fps",
])  # fmt: skip
def test_parse_args_fps_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)


@pytest.mark.parametrize("value, expected", [
    ("0.000001", 0.000001),
    ("0.1", 0.1),
    ("1", 1),
    ("1.0", 1.0),
    ("2", 2),
    ("10", 10),
    ("100", 100),
    ("10000000", 10000000),
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-f",
    "--frequency",
])  # fmt: skip
def test_parse_args_frequency_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.frequency == expected


@pytest.mark.parametrize("value", [
    "",
    "0",
    "-1",
    "-1.0",
    "not a numeric value",
],)  # fmt: skip
@pytest.mark.parametrize("arg", [
    "-f",
    "--frequency",
])  # fmt: skip
def test_parse_args_frequency_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)


@pytest.mark.parametrize("value, expected", [
    ("1.1.1.1", ipaddress.ip_address("1.1.1.1")),
    ("192.168.5.1", ipaddress.ip_address("192.168.5.1")),
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "--dst",
])  # fmt: skip
def test_parse_args_dst_ip_address_valid(arg, value, expected):
    parsed = helper_parse_args(arg, value)
    assert parsed.dst == expected


@pytest.mark.parametrize("value", [
    "",
    "1",
    "1.1.1",
    "192.168.1.1000",
    "192.168.1.a",
    "a.a.a.a",
])  # fmt: skip
@pytest.mark.parametrize("arg", [
    "--dst",
])  # fmt: skip
def test_parse_args_dst_ip_address_invalid(arg, value):
    with pytest.raises(SystemExit):
        helper_parse_args(arg, value)
