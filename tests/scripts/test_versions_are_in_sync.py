# pylint: skip-file

import sys
from pathlib import Path

import toml

import ray_cli


def test_versions_are_in_sync():
    """Checks if the pyproject.toml and package.__init__.py __version__ are in sync."""
    path = Path(__file__).resolve().parents[2] / "pyproject.toml"

    pyproject = toml.loads(open(str(path)).read())
    pyproject_version = pyproject["tool"]["poetry"]["version"]
    package_init_version = ray_cli.__version__

    assert package_init_version == pyproject_version


if __name__ == "__main__":
    try:
        test_versions_are_in_sync()
        sys.exit(0)

    except AssertionError:
        sys.exit(1)
