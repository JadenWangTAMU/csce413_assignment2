#!/bin/sh
set -e

# Ensure sshd runtime dir exists (defensive)
mkdir -p /var/run/sshd

# Block SSH until knock
iptables -A INPUT -p tcp --dport 2222 -j DROP

# Start SSH as a daemon (master stays alive)
/usr/sbin/sshd

# Start knock server as PID 1
exec python3 /app/knock_server.py
