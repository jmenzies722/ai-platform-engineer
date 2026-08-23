#!/usr/bin/env python3
"""Run a bounded workload that remains available for process inspection."""

from __future__ import annotations

import argparse
import hashlib
import os
import signal
import sys
import time


stop_requested = False


def request_stop(signum: int, _frame: object) -> None:
    """Request an orderly stop after receiving a terminal signal."""
    global stop_requested
    stop_requested = True
    print(f"received signal={signum}; stopping", file=sys.stderr, flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seconds",
        type=int,
        default=90,
        choices=range(5, 601),
        metavar="5..600",
        help="maximum run time (default: 90)",
    )
    parser.add_argument(
        "--memory-mib",
        type=int,
        default=32,
        choices=range(1, 257),
        metavar="1..256",
        help="memory to allocate and touch (default: 32 MiB)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    print(
        f"pid={os.getpid()} ppid={os.getppid()} executable={sys.executable}",
        flush=True,
    )
    print(
        f"stdout_isatty={sys.stdout.isatty()} "
        f"requested_memory_mib={args.memory_mib}",
        flush=True,
    )

    # bytearray commits address space; touching one byte per typical 4 KiB page
    # makes resident-memory growth visible without relying on page size.
    payload = bytearray(args.memory_mib * 1024 * 1024)
    for offset in range(0, len(payload), 4096):
        payload[offset] = offset % 251

    # A short, bounded CPU phase gives process tools a nonzero CPU-time sample.
    digest = b"execution-lab"
    for _ in range(250_000):
        digest = hashlib.sha256(digest).digest()
    print(f"allocation_touched=true digest_prefix={digest.hex()[:12]}", flush=True)

    deadline = time.monotonic() + args.seconds
    heartbeat = 0
    while not stop_requested and time.monotonic() < deadline:
        print(f"heartbeat={heartbeat}", file=sys.stderr, flush=True)
        heartbeat += 1
        time.sleep(5)

    # Keep payload live until inspection is complete.
    print(f"exiting payload_bytes={len(payload)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
