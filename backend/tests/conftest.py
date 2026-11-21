"""Pytest test session configuration.

Ensures that automated test runs never leave mock/fake test rows (such as test invoices,
mock leads, test customer reviews, mock change requests, or test execution workspaces)
inside the active PostgreSQL database.
"""

import os
import subprocess
import sys


def pytest_sessionfinish(session, exitstatus):
    """Automatically run clean_fake_data in a clean process after tests finish."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(base_dir, "scripts", "clean_fake_data.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir

    try:
        subprocess.run(
            [sys.executable, script_path],
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        print(f"Warning during post-test cleanup: {exc}")
