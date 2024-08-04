# Ray CLI

Command line utility for generating and broadcast DMX over sACN.

[![GitHub Release](https://img.shields.io/github/v/release/nobbmaestro/ray-cli)](github-release)
[![GitHub last commit](https://img.shields.io/github/last-commit/nobbmaestro/ray-cli/development)](github-last-commit)
[![GitHub commits since](https://img.shields.io/github/commits-since/nobbmaestro/ray-cli/v0.2.0/development)](githut-commits-since)
![Tests](https://github.com/nobbmaestro/ray-cli/actions/workflows/tests.yml/badge.svg)

## Installation

### Pip

```sh
pip install ray-cli
```

### GitHub

```sh
git clone git@github.com:nobbmaestro/ray-cli.git
cd ray-cli
make install
```

## Usage

```console
$ ray-cli --help
usage: ray-cli [-m {chase,ramp,ramp-down,ramp-up,sine,square,static}] [-d DURATION]
               [-u UNIVERSES [UNIVERSES ...]] [-c CHANNELS] [-i INTENSITY]
               [-f FREQUENCY] [--fps FPS] [--dst DST] [-v] [-q] [--dry] [-h]
                [--version] IP_ADDRESS

Command line utility for generating and broadcast DMX over sACN.

positional arguments:
  IP_ADDRESS            IP address of the dmx source

optional arguments:
  -m {chase,ramp,ramp-down,ramp-up,sine,square,static},
  --mode {chase,ramp,ramp-down,ramp-up,sine,square,static}
                        broadcast mode, defaults to ramp
  -d DURATION, --duration DURATION
                        broadcast duration in seconds, defaults to INDEFINITE
  -u UNIVERSES [UNIVERSES ...], --universes UNIVERSES [UNIVERSES ...]
                        sACN universe(s) to send to
  -c CHANNELS, --channels CHANNELS
                        DMX channels at universe to send to, (1, ...512)
  -i INTENSITY, --intensity INTENSITY
                        DMX channels output intensity, (1, ...255)
  -f FREQUENCY, --frequency FREQUENCY
                        signal frequency
  --fps FPS             frames per second per universe
  --dst DST             IP address of the dmx destination, defaults to MULTICAST

display options:
  -v, --verbose         run in verbose mode
  -q, --quiet           run in quiet mode

operational options:
  --dry                 simulate outputs without broadcasting (dry run mode), assumes
                        verbose mode

query options:
  -h, --help            print help and exit
  --version             show program's version number and exit

```
