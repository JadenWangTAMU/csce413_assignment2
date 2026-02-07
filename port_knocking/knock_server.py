#!/usr/bin/env python3
"""Starter template for the port knocking server."""

import argparse
import logging
import socket
import time
import threading
import subprocess

DEFAULT_KNOCK_SEQUENCE = [1560, 6580, 8153]
DEFAULT_PROTECTED_PORT = 2222
DEFAULT_SEQUENCE_WINDOW = 10.0

# Tracks progress per IP: { ip: { "index": int, "last_time": float } }
client_progress = {}

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def open_protected_port(protected_port, ip):
    """Open the protected port using firewall rules."""
    # TODO: Use iptables/nftables to allow access to protected_port.
    logging.info("Opening firewall for %s on port %s", ip, protected_port)
    subprocess.run(["iptables", "-I", "INPUT", "-p", "tcp", "--dport", str(protected_port), "-s", ip, "-j", "ACCEPT"])
    logging.info("Port %s opened for %s", protected_port, ip)


def close_protected_port(protected_port):
    """Close the protected port using firewall rules."""
    # TODO: Remove firewall rules for protected_port.
    logging.info("Closing firewall for port %s", protected_port)
    subprocess.run(["iptables", "-D", "INPUT", "-p", "tcp", "--dport", str(protected_port), "-j", "ACCEPT"])
    logging.info("Port %s closed", protected_port)

def listen_on_port(port, sequence, window_seconds, protected_port):
    """Listen for knocks on a single port."""
    logger = logging.getLogger("KnockServer")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    
    logger.info("Listening on knock port %s", port)
    
    while True:
        data, addr = sock.recvfrom(1024)
        ip = addr[0]
        now = time.time()

        # Initialize tracking for new IPs
        if ip not in client_progress:
            client_progress[ip] = {"index": 0, "last_time": now}
        
        # Reset if too slow
        if now - client_progress[ip]["last_time"] > window_seconds:
            client_progress[ip]["index"] = 0
        
        expected_port = sequence[client_progress[ip]["index"]]
        
        if port == expected_port:
            client_progress[ip]["index"] += 1
            client_progress[ip]["last_time"] = now
            logger.info("%s knocked correctly on %s", ip, port)
            
            # Sequence complete
            if client_progress[ip]["index"] == len(sequence):
                logger.info("Correct sequence from %s!", ip)
                open_protected_port(protected_port, ip)
                client_progress[ip]["index"] = 0
        
        else:
            logger.info("%s knocked wrong port %s (expected %s). Resetting.", ip, port, expected_port)
            client_progress[ip]["index"] = 0

def listen_for_knocks(sequence, window_seconds, protected_port):
    """Listen for knock sequence and open the protected port."""
    logger = logging.getLogger("KnockServer")
    logger.info("Listening for knocks: %s", sequence)
    logger.info("Protected port: %s", protected_port)

    # TODO: Create UDP or TCP listeners for each knock port.
    # TODO: Track each source IP and its progress through the sequence.
    # TODO: Enforce timing window per sequence.
    # TODO: On correct sequence, call open_protected_port().
    # TODO: On incorrect sequence, reset progress.
    logger = logging.getLogger("KnockServer")
    logger.info("Knock sequence: %s", sequence)
    logger.info("Protected port: %s", protected_port)
    logger.info("Sequence window: %s seconds", window_seconds)
    
    # Start a thread for each knock port
    for port in sequence:
        t = threading.Thread(target=listen_on_port, args=(port, sequence, window_seconds, protected_port), daemon=True)
        t.start()

    while True:
        time.sleep(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Port knocking server starter")
    parser.add_argument(
        "--sequence",
        default=",".join(str(port) for port in DEFAULT_KNOCK_SEQUENCE),
        help="Comma-separated knock ports",
    )
    parser.add_argument(
        "--protected-port",
        type=int,
        default=DEFAULT_PROTECTED_PORT,
        help="Protected service port",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=DEFAULT_SEQUENCE_WINDOW,
        help="Seconds allowed to complete the sequence",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()

    try:
        sequence = [int(port) for port in args.sequence.split(",")]
    except ValueError:
        raise SystemExit("Invalid sequence. Use comma-separated integers.")

    listen_for_knocks(sequence, args.window, args.protected_port)


if __name__ == "__main__":
    main()