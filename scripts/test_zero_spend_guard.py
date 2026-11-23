import os
import socket
import subprocess
import sys
from pathlib import Path

from zero_spend_guard import paid_sandbox_enabled

ROOT = Path(__file__).resolve().parents[1]


def test_provider_keys_are_scrubbed():
    assert os.environ.get("GEMINI_API_KEY") is None
    assert os.environ.get("DEEPSEEK_API_KEY") is None
    assert os.environ.get("ELEVENLABS_API_KEY") is None


def test_outbound_socket_blocked():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        try:
            sock.connect(("1.1.1.1", 443))
        except OSError as exc:
            assert "ZERO_SPEND_GUARD" in str(exc)
        else:
            raise AssertionError("outbound socket was allowed")
    finally:
        sock.close()


def test_dns_lookup_blocked():
    try:
        socket.getaddrinfo("example.com", 443)
    except OSError as exc:
        assert "ZERO_SPEND_GUARD" in str(exc)
    else:
        raise AssertionError("outbound DNS was allowed")


def test_loopback_is_not_policy_blocked():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        try:
            sock.connect(("127.0.0.1", 9))
        except OSError as exc:
            assert "ZERO_SPEND_GUARD" not in str(exc)
    finally:
        sock.close()


def test_paid_sandbox_needs_both_switches(monkeypatch):
    monkeypatch.delenv("ALLOW_PAID_SANDBOX", raising=False)
    assert paid_sandbox_enabled(True) is False
    monkeypatch.setenv("ALLOW_PAID_SANDBOX", "1")
    assert paid_sandbox_enabled(False) is False
    assert paid_sandbox_enabled(True) is True


def _run_child(extra_args, env):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "scripts/test_zero_spend_guard.py",
            "-k",
            "test_outbound_socket_blocked",
            *extra_args,
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_one_opt_in_does_not_open_sockets():
    base = os.environ.copy()
    base["TC_ZERO_SPEND_CHILD"] = "1"
    for key in ("GEMINI_API_KEY", "DEEPSEEK_API_KEY", "ELEVENLABS_API_KEY"):
        base.pop(key, None)

    flagged = base.copy()
    flagged.pop("ALLOW_PAID_SANDBOX", None)
    only_flag = _run_child(["--live-sandbox"], flagged)
    assert only_flag.returncode == 0, only_flag.stdout + only_flag.stderr

    only_env = base.copy()
    only_env["ALLOW_PAID_SANDBOX"] = "1"
    only_env_run = _run_child([], only_env)
    assert only_env_run.returncode == 0, only_env_run.stdout + only_env_run.stderr
