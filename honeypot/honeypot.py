#!/usr/bin/env python3
"""Starter template for the honeypot assignment."""

import socket
import logging
import os
import time
from logger import create_logger

HOST = "0.0.0.0"
PORT = 22
BANNER = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n"

def handle_client(conn, addr):
    ip, port = addr
    start = time.time()
    logger = logging.getLogger("Honeypot")

    logger.info(f"Connection from {ip}:{port}")

    try:
        # Send fake SSH banner
        conn.sendall(BANNER)

        # Read whatever the client sends
        while True:
            data = conn.recv(1024)
            if not data:
                break
            logger.info(f"Data from {ip}:{port}: {data!r}")

    except Exception as e:
        logger.info(f"Error with {ip}:{port}: {e}")

    finally:
        duration = time.time() - start
        logger.info(f"Connection closed from {ip}:{port} (duration {duration:.2f}s)")
        conn.close()

def run_honeypot():
    logger = logging.getLogger("Honeypot")
    logger.info("Honeypot running on port 22")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(50)

    while True:
        conn, addr = sock.accept()
        handle_client(conn, addr)

if __name__ == "__main__":
    create_logger()
    run_honeypot()
