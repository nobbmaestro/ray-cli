import subprocess
import sys

import pytest


@pytest.mark.integration_tests
def test_integration():
    cmd = [
        sys.executable,
        "-m",
        "ray_cli",
        "--version",
    ]

    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as p:
        _, stderr = p.communicate()

        assert p.returncode == 0, stderr.decode()
