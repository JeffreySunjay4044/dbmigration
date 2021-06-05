FROM debezium/postgres:11

LABEL maintainer="Debezium Community"

COPY inventory.sql /docker-entrypoint-initdb.d/
COPY port_forwarding.sh /opt/scripts/port_forwarding.sh
RUN  apt-get update &&  apt-get install openssh-server && chmod 600 xxx.pem
RUN ["chmod", "+x", "/opt/scripts/port_forwarding.sh"]
