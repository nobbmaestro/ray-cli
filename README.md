# Ray CLI

Command line utility for generating and broadcast DMX over sACN.

[![GitHub Release](https://img.shields.io/github/v/release/nobbmaestro/ray-cli)](github-release)
[![GitHub last commit](https://img.shields.io/github/last-commit/nobbmaestro/ray-cli/development)](github-last-commit)
[![GitHub commits since](https://img.shields.io/github/commits-since/nobbmaestro/ray-cli/v0.3.0/development)](githut-commits-since)
![Tests](https://github.com/nobbmaestro/ray-cli/actions/workflows/tests.yml/badge.svg)

## Installation

### Pipx (Recommended)

```sh
pipx install ray-cli
```

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
usage: ray-cli [-m {chase,ramp,ramp-down,ramp-up,sine,square,static}]
               [-d DURATION] [-u UNIVERSES [UNIVERSES ...]] [-c CHANNELS]
               [-i INTENSITY] [-f FREQUENCY] [--fps FPS] [--dst DST] [-v] [-q]
               [--dry] [-h] [-V]
               IP_ADDRESS

Command line utility for generating and broadcast DMX over sACN

positional arguments:
  IP_ADDRESS                                 IP address of the DMX source

options:
  -m, --mode {chase,ramp,ramp-down,ramp-up,sine,square,static}
                                             DMX signal shape mode (default:
                                             ramp)
  -d, --duration DURATION                    broadcast duration in seconds
                                             (default: INDEFINITE)
  -u, --universes UNIVERSES [UNIVERSES ...]  sACN universe(s) to send to
                                             (default: 1)
  -c, --channels CHANNELS                    DMX channels at universe to send to
                                             (range: 1-512, default: 24)
  -i, --intensity INTENSITY                  DMX channels output intensity
                                             (range: 1-255, default: 10)
  -f, --frequency FREQUENCY                  frequency of the generated signal
                                             (default: 1.0)
  --fps FPS                                  frames per second per universe
                                             (default: 10)
  --dst DST                                  IP address of the dmx destination
                                             (default: MULTICAST)

display options:
  -v, --verbose                              run in verbose mode
  -q, --quiet                                run in quiet mode

operational options:
  --dry                                      simulate outputs without broadcast

query options:
  -h, --help                                 print help and exit
  -V, --version                              show program's version number and
                                             exit
```
