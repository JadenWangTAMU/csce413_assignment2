#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""

import socket
import sys
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_SERVICES = { 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis", 5001: "Flask Web App" }

def identify_service(port, banner):
    """Return service name based on banner or port number."""
    if banner:
        b=banner.lower()
        if "ssh" in b:
            return "SSH"
        if "redis" in b:
            return "Redis"
        if "<html" in b or "doctype html" in b:
            return "HTTP"
        if "mysql" in b:
            return "MySQL"
        return banner.strip()
    return COMMON_SERVICES.get(port, "Unknown")

def scan_port(target, port, timeout=1.0):
    """
    Scan a single port on the target host

    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to scan
        timeout (float): Connection timeout in seconds

    Returns:
        bool: True if port is open, False otherwise
    """
    start_time = time.time()
    banner = None
    
    try:
        # TODO: Create a socket
        # TODO: Set timeout
        # TODO: Try to connect to target:port
        # TODO: Close the socket
        # TODO: Return True if connection successful

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))

            if result == 0:
                try:
                    s.sendall(b"HELLO\r\n")
                    banner = s.recv(1024).decode(errors="ignore").strip()
                except Exception:
                    banner = None

                elapsed = round(time.time() - start_time, 3)
                return {
                    "port": port,
                    "state": "open",
                    "time": elapsed,
                    "banner": banner,
                    "service": identify_service(port, banner)
                }

    except (socket.timeout, ConnectionRefusedError, OSError):
        pass
    except OSError:
        pass

    return None


def scan_range(target, start_port, end_port, threads):
    """
    Scan a range of ports on the target host

    Args:
        target (str): IP address or hostname to scan
        start_port (int): Starting port number
        end_port (int): Ending port number

    Returns:
        list: List of open ports
    """
    open_ports = []

    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    print(f"[*] This may take a while...")

    # TODO: Implement the scanning logic
    # Hint: Loop through port range and call scan_port()
    # Hint: Consider using threading for better performance

    # for port in range(start_port, end_port + 1):
        # TODO: Scan this port
        # TODO: If open, add to open_ports list
        # TODO: Print progress (optional)
        # pass  # Remove this and implement

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, target, port): port
            for port in range(start_port, end_port + 1)
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
                print(f"[+] Port {result['port']} OPEN ({result['time']}s)")
                if result["banner"]:
                    print(f"    Banner: {result['banner']}")
                if result["service"]:
                    print(f"    Service: {result['service']}")

    return open_ports


def main():
    """Main function"""
    # TODO: Parse command-line arguments
    # TODO: Validate inputs
    # TODO: Call scan_range()
    # TODO: Display results

    # # Example usage (you should improve this):
    # if len(sys.argv) < 2:
    #     print("Usage: python3 port_scanner_template.py <target>")
    #     print("Example: python3 port_scanner_template.py 172.20.0.10")
    #     sys.exit(1)

    # target = sys.argv[1]
    # start_port = 1
    # end_port = 1024  # Scan first 1024 ports by default

    # print(f"[*] Starting port scan on {target}")

    # open_ports = scan_range(target, start_port, end_port)

    # print(f"\n[+] Scan complete!")
    # print(f"[+] Found {len(open_ports)} open ports:")
    # for port in open_ports:
    #     print(f"    Port {port}: open")

    parser = argparse.ArgumentParser(description="Custom TCP Port Scanner")
    parser.add_argument("--target", required=True, help="Target IP or hostname")
    parser.add_argument("--ports", required=True, help="Port range (e.g. 1-10000)")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads")

    args = parser.parse_args()

    try:
        start_port, end_port = map(int, args.ports.split("-"))
    except ValueError:
        print("[-] Invalid port range format. Use start-end (e.g. 1-1024)")
        return
    
    try:
        socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[-] Could not resolve hostname: {args.target}")
        return

    print(f"[*] Starting scan on {args.target}")
    total_start = time.time()

    results = scan_range(args.target, start_port, end_port, args.threads)

    total_time = round(time.time() - total_start, 2)
    print("\n[+] Scan complete")
    print(f"[+] {len(results)} open ports found")
    print(f"[+] Total scan time: {total_time}s\n")

    for r in sorted(results, key=lambda x: x["port"]):
        print(
            f"Port {r['port']} | OPEN | {r['time']}s | "
            f"Banner: {r['banner'] if r['banner'] else 'Unknown'} | "
            f"Service: {r['service'] if r['service'] else 'Unknown'}"
        )


if __name__ == "__main__":
    main()
