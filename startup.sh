#!/usr/bin/env bash

IMG_NAME=my_servers:v0.0.3
SERVER_NAME=my_servers

# HTTP
PORTS_FLAGS="-p 80:80"
# HTTPS
PORTS_FLAGS=$PORTS_FLAGS" -p 443:443"
# FTP
PORTS_FLAGS=$PORTS_FLAGS" -p 21:21"
PORTS_FLAGS=$PORTS_FLAGS" -p 12000-12100:12000-12100"
# NFS
if [ -n "$(echo $1 $2 | grep nfs)" ]; then
    PORTS_FLAGS=$PORTS_FLAGS" -p 111:111 -p 2049:2049"
fi
# SAMBA
if [ -n "$(echo $1 $2 | grep samba)" ]; then
    PORTS_FLAGS=$PORTS_FLAGS" -p 137:137 -p 138:138 -p 139:139 -p 445:445"
fi

# Metric 
PORTS_FLAGS=$PORTS_FLAGS" -p 5000:5000"


#HTTP/HTTPS
CONFIG_MOUNT="-v $(pwd)/HTTP:/root/HTTP  -v $(pwd)/HTTPS:/root/HTTPS"
#FTP
CONFIG_MOUNT=${CONFIG_MOUNT}" -v $(pwd)/FTP:/root/FTP"
# NFS
CONFIG_MOUNT=${CONFIG_MOUNT}" -v $(pwd)/NFS:/root/NFS"
# SAMBA
CONFIG_MOUNT=${CONFIG_MOUNT}" -v $(pwd)/SAMBA:/root/SAMBA"

docker run -it --privileged  $PORTS_FLAGS $CONFIG_MOUNT  --name $SERVER_NAME $IMG_NAME $@
docker rm $SERVER_NAME
