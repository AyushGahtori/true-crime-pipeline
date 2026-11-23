"""Block outbound sockets and scrub provider keys during ordinary pytest runs.

Paid sockets stay closed unless the process was started with both
``--live-sandbox`` and ``ALLOW_PAID_SANDBOX=1``.
"""

from __future__ import annotations

import os
import socket

SCRUBBED_ENV = ("GEMINI_API_KEY", "DEEPSEEK_API_KEY", "ELEVENLABS_API_KEY")

_INSTALLED = False
_REAL_GETADDRINFO = socket.getaddrinfo
_REAL_CREATE_CONNECTION = socket.create_connection


def paid_sandbox_enabled(live_flag: bool) -> bool:
    return bool(live_flag) and os.environ.get("ALLOW_PAID_SANDBOX") == "1"


def _host_of(address: object) -> object:
    if isinstance(address, tuple) and address:
        return address[0]
    return address


def _text(host: object) -> str:
    if isinstance(host, bytes):
        return host.decode("ascii", "ignore")
    return str(host)


def _is_loopback(host: object) -> bool:
    if host is None or host == "":
        return True
    return _text(host).strip("[]").lower() in {"127.0.0.1", "::1", "localhost"}


def _is_ip_literal(host: object) -> bool:
    text = _text(host)
    try:
        socket.inet_aton(text)
        return True
    except OSError:
        return ":" in text


def _reject(address: object) -> None:
    if _is_loopback(_host_of(address)):
        return
    raise OSError(f"ZERO_SPEND_GUARD: blocked outbound socket to {address!r}")


class _GuardedSocket(socket.socket):
    def connect(self, address):  # type: ignore[override]
        _reject(address)
        return super().connect(address)

    def connect_ex(self, address):  # type: ignore[override]
        _reject(address)
        return super().connect_ex(address)

    def sendto(self, data, *args):  # type: ignore[override]
        if args and isinstance(args[-1], tuple):
            _reject(args[-1])
        return super().sendto(data, *args)


def _guarded_getaddrinfo(host, port, *args, **kwargs):
    if host and not _is_loopback(host) and not _is_ip_literal(host):
        raise OSError(f"ZERO_SPEND_GUARD: blocked DNS lookup for {host!r}")
    return _REAL_GETADDRINFO(host, port, *args, **kwargs)


def _guarded_create_connection(address, *args, **kwargs):
    _reject(address)
    return _REAL_CREATE_CONNECTION(address, *args, **kwargs)


def install_socket_block() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    socket.socket = _GuardedSocket  # type: ignore[misc, assignment]
    socket.getaddrinfo = _guarded_getaddrinfo  # type: ignore[assignment]
    socket.create_connection = _guarded_create_connection  # type: ignore[assignment]
    _INSTALLED = True


def scrub_provider_env() -> None:
    for key in SCRUBBED_ENV:
        os.environ.pop(key, None)


def pytest_addoption(parser):
    parser.addoption(
        "--live-sandbox",
        action="store_true",
        default=False,
        help="Allow paid provider sockets only together with ALLOW_PAID_SANDBOX=1.",
    )


def pytest_configure(config):
    live = bool(config.getoption("--live-sandbox"))
    if paid_sandbox_enabled(live):
        return
    scrub_provider_env()
    install_socket_block()
