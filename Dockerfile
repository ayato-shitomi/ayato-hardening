FROM ubuntu:23.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apache2 \
    openssh-server \
    build-essential \
    python3 \
    python3-pip \
    python3-flask \
    net-tools \
    ufw \
    openssh-server \
    && apt-get clean

COPY blue-team /blue-team
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

EXPOSE 21 22 80 8080 6200

CMD ["./blue-team/run.sh"]