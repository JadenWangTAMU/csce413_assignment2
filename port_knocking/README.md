## Port Knocking Starter Template

This directory is a starter template for the port knocking portion of the assignment.

### What you need to implement
- Pick a protected service/port (default is 2222).
- Define a knock sequence (e.g., 1234, 5678, 9012).
- Implement a server that listens for knocks and validates the sequence.
- Open the protected port only after a valid sequence.
- Add timing constraints and reset on incorrect sequences.
- Implement a client to send the knock sequence.

### Getting started
1. Implement your server logic in `knock_server.py`.
2. Implement your client logic in `knock_client.py`.
3. Update `demo.sh` to demonstrate your flow.
4. Run from the repo root with `docker compose up port_knocking`.

### Example usage
```bash
python3 knock_client.py --target 172.20.0.40 --sequence 1234,5678,9012
```

This project implements a simple port‑knocking mechanism using Python and iptables.
A client sends a sequence of UDP “knocks” to predefined ports.
If the sequence is correct and completed within a time window, the server dynamically opens a protected TCP port for the client’s IP address.
This version intentionally avoids SSH entirely and instead protects a simple TCP listener running on port 2222.

1. knock_server.py
Listens on three UDP ports: 1560, 6580, 8153
Tracks each client’s progress through the knock sequence
Enforces a timing window
On correct sequence: Inserts an iptables rule allowing the client’s IP to access TCP port 2222

2. knock_client.py
Sends the knock sequence to the server
Optionally attempts to connect to the protected port afterward
Uses UDP packets for knocking and a TCP connection for verification

3. entrypoint.sh
Blocks TCP port 2222 by default
Starts a simple TCP listener using nc -lkp 2222
Starts the knock server as PID 1

4. Dockerfile
Installs Python, iptables, and netcat
Exposes the knock ports and protected port
Runs the entrypoint script

5. Open the Terminal, Navigate to the port_knocking directory, and Build the image: docker build -t portknock .

6. Run the container: docker run --rm -it --cap-add=NET_ADMIN -p 1560:1560/udp -p 6580:6580/udp -p 8153:8153/udp -p 2222:2222/tcp portknock
The container will:
Block TCP port 2222
Start a TCP listener on port 2222
Start the knock server
Log all knock activity

7. Open another Terminal and Test the Knock Sequence: python3 knock_client.py --target 127.0.0.1 --check
Expected behavior:
The client sends UDP knocks to ports 1560 → 6580 → 8153
The server logs each correct knock
After the full sequence, the server inserts an iptables ACCEPT rule
The client successfully connects to TCP port 2222
The demo script prints:
[*] Sending knock sequence: [1560, 6580, 8153]
[*] Knocking on port 1560
[*] Knocking on port 6580
[*] Knocking on port 8153
[+] Knock sequence complete
[*] Checking access to protected port 2222...
[+] Connected to protected port 2222
