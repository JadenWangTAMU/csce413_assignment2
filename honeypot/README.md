## Honeypot Starter Template

This directory is a starter template for the honeypot portion of the assignment.

### What you need to implement
- Choose a protocol (SSH, HTTP, or multi-protocol).
- Simulate a convincing service banner and responses.
- Log connection metadata, authentication attempts, and attacker actions.
- Store logs under `logs/` and include an `analysis.md` summary.
- Update `honeypot.py` and `logger.py` (and add modules as needed) to implement the honeypot.

### Getting started
1. Implement your honeypot logic in `honeypot.py`.
2. Wire logging in `logger.py` and record results in `logs/`.
3. Summarize your findings in `analysis.md`.
4. Run from the repo root with `docker-compose up honeypot`.

The honeypot listens on TCP port 22 and presents a realistic OpenSSH banner to any connecting client.
This causes SSH clients and automated scanners to behave as if they are interacting with a legitimate SSH server.

Simulated SSH Service:
Listens on port 22 inside the container
Sends a realistic OpenSSH banner
Accepts TCP connections
Causes SSH clients to initiate normal handshake behavior

Logging:
Source IP address and port
Timestamp of connection
Connection duration
SSH client banner
All data sent by the client
Written to logs/honeypot.log

Stealth:
The honeypot does not reveal itself as a decoy
SSH clients hang during key exchange, which is consistent with a misconfigured or overloaded SSH server

Running:
Build the image: docker build -t honeypot .
Run the honeypot: docker run --rm -it -p 2222:22 -v $(pwd)/logs:/app/logs honeypot (to ensure logs are written to honeypot.log)
You should see: Honeypot running on port 22

Testing:
Run in another terminal: ssh admin@localhost -p 2222
The SSH client will hang (expected), and the honeypot will log all data sent during the handshake.