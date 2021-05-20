#!/bin/bash

if [ "$SAMBA_CLIENT" == yes ]
then
    mkdir -p /config/workspace
    mount -t cifs //${SAMBA_IP}/iot-data /config/workspace \
        -osec=ntlmssp,domain=WORKGROUP,username=root,password=${SAMBA_PASSWORD},uid=$(id -u),gid=$(id -g)
fi

if [ -f ${IOT}/bin/start-${BALENA_SERVICE_NAME}.sh ]; then
    /bin/bash ${IOT}/bin/start-${BALENA_SERVICE_NAME}.sh
fi
