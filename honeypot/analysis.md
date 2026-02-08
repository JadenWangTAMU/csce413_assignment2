# Honeypot Analysis
Deployed as a SSH‑like service listening on port 22 inside a Docker container.
Presented a realistic OpenSSH banner and accepted TCP connections.
Ensured that attackers behaved as if they were connecting to a legitimate SSH server, capturing early‑stage SSH negotiation data.

During testing, successfully logged all incoming connections, including timestamps, source IP addresses, and raw data sent by the SSH client.
Remained stable throughout testing and did not reveal itself as a decoy.

## Summary of Observed Attacks
Test attack: ssh admin@localhost -p 2222
The honeypot recorded the following behaviors:
The SSH client connected and sent its identification string: SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.14
The client immediately initiated SSH key‑exchange negotiation.
Multiple binary packets were sent containing: Supported key‑exchange algorithms, Encryption and MAC algorithms, Compression methods, Protocol extensions
The client hung after sending negotiation data because the honeypot did not respond with valid SSH protocol messages.
The honeypot logged the full duration of the connection before the client timed out.

## Notable Patterns
Consistent SSH negotiation behavior: Every connection began with a banner exchange followed by a large binary KEXINIT packet.
Binary data transmission: The majority of logged data consisted of raw binary packets.
Client timeout behavior: Since the honeypot does not complete the SSH handshake, the client eventually hangs and disconnects.
No credential attempts captured: Because the SSH handshake never progresses to authentication, no usernames or passwords were logged.

I did not implement a SSH handshake because I faced many SSHD issues while working in Port Scanner.
I eventually concluded that there was a Docker network namespace isolation issue. A healthy sshd process tree looks like:
"/usr/sbin/sshd -D
sshd: /usr/sbin/sshd [listener]
sshd: root@pts/0:"
But my sshd process tree looks like:
"sshd: /usr/sb"
which is the privilege seperation child which cannot accept connections.

I confirmed that my ssh_config was valid, host keys exist, PAM is stock, /var/run/sshd exists, iptables rules are correct, knock_server opens the firewall correctly, knock client sends correct UDP packets, the container exposts the correct ports, Docker maps the ports correctly, the entrypoint starts sshd correctly, the knock server runs as PID 1, the port appears open, ssh is listening, and the firewall rule is inserted.
But the master sshd process crashes immediately.

## Recommendations
Implement deeper SSH emulation: Simulating enough of the SSH handshake to reach the authentication stage would allow the honeypot to capture usernames and password attempts.
Add connection timeouts or auto‑disconnect logic: This prevents long‑running hung sessions and keeps logs cleaner.
Introduce basic alerting: For example, flag repeated connection attempts from the same IP or known malicious SSH banners.
Support multiple protocols: Adding HTTP or Telnet honeypot behavior would broaden the attack surface and capture more diverse activity.
Store logs in structured format (JSON): This would make later analysis easier and more automated.