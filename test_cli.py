import subprocess
import sys
import pytest


def test_cli_list_no_server():
    """Should NOT crash with an unhandled exception."""
    result = subprocess.run(
        [sys.executable, "cli.py", "list"],
        capture_output=True, text=True, timeout=10,
    )
    # Should not show a raw Python traceback
    output = result.stdout + result.stderr
    assert "Traceback" not in output
    assert len(output.strip()) > 0


def test_cli_run_no_server():
    """Should NOT crash with an unhandled exception."""
    result = subprocess.run(
        [sys.executable, "cli.py", "run", "somemodel.gguf", "hello"],
        capture_output=True, text=True, timeout=10,
    )
    output = (result.stdout + result.stderr).lower()
    # Should not show a raw Python traceback
    assert "traceback" not in output
    # Should contain some human-readable message
    assert "not running" in output or "error" in output or "not found" in output


def test_cli_delete_cancel():
    result = subprocess.run(
        [sys.executable, "cli.py", "delete", "somemodel.gguf"],
        input="n\n", capture_output=True, text=True, timeout=10,
    )
    output = result.stdout + result.stderr
    assert "Cancelled" in output
