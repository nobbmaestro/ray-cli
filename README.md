# Ray CLI

Command line utility for generating and broadting DMX over sACN.

[![GitHub Release](https://img.shields.io/github/v/release/nobbmaestro/ray-cli)](github-release)
[![GitHub last commit](https://img.shields.io/github/last-commit/nobbmaestro/ray-cli/development)](github-last-commit)
[![GitHub commits since](https://img.shields.io/github/commits-since/nobbmaestro/ray-cli/v0.6.0/development)](githut-commits-since)

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

```sh
$ ray-cli --help
usage: ray-cli [-m {static,chase,ramp}] [-d DURATION] [-u UNIVERSES [UNIVERSES ...]]
               [-c CHANNELS] [-i INTENSITY] [-f FREQUENCY] [--fps FPS] [--dst DST]
               [-v] [-q] [-h] [--version] IP_ADDRESS

Command line utility for generating and broadcast DMX over sACN.

positional arguments:
  IP_ADDRESS            IP address of the dmx source

optional arguments:
  -m {static,chase,ramp}, --mode {static,chase,ramp}
                        broadcast mode, defaults to ramp
  -d DURATION, --duration DURATION
                        broadcast duration in seconds, defaults to INDEFINITE
  -u UNIVERSES [UNIVERSES ...], --universes UNIVERSES [UNIVERSES ...]
                        sACN universe(s) to send to
  -c CHANNELS, --channels CHANNELS
                        DMX channels at universe to send to, (0, ...512)
  -i INTENSITY, --intensity INTENSITY
                        DMX channels output intensity, (0, ...255)
  -f FREQUENCY, --frequency FREQUENCY
                        signal frequency
  --fps FPS             frames per second per universe
  --dst DST             IP address of the dmx destination, defaults to MULTICAST

display options:
  -v, --verbose         run in verbose mode
  -q, --quiet           run in quiet mode

query options:
  -h, --help            print help and exit
  --version             show program's version number and exit

```
