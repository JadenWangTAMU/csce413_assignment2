#!/bin/sh
set -e

# Block protected port until knock
iptables -A INPUT -p tcp --dport 2222 -j DROP

# Start a simple TCP listener on port 2222
# This will accept connections once the firewall rule is opened
nc -lkp 2222 >/dev/null 2>&1 &

# Start knock server (PID 1)
exec python3 /app/knock_server.py