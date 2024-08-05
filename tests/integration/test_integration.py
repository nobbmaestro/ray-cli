import subprocess
import sys

import pytest


@pytest.mark.timeout(10)
@pytest.mark.integration_tests
def test_integration():
    cmd = [
        sys.executable,
        "-m",
        "ray_cli",
        "192.168.5.1",
        "--duration",
        "1",
        "--quiet",
    ]

    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as p:
        _, stderr = p.communicate()

        assert p.returncode == 0, stderr
