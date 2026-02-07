FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        iptables \
        iproute2 \
        openssh-server \
    && rm -rf /var/lib/apt/lists/*

# SSH base setup
RUN mkdir -p /var/run/sshd \
    && ssh-keygen -A \
    && echo "root:root" | chpasswd \
    && sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config \
    && sed -i 's/^#PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config

COPY knock_server.py knock_client.py entrypoint.sh ./

# Expose knock ports + protected port
EXPOSE 1560/udp
EXPOSE 6580/udp
EXPOSE 8153/udp
EXPOSE 2222/tcp

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
