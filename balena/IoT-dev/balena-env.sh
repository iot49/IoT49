#! /bin/bash

# fleet wide environment

balena env add SHELL          "/bin/bash"            --application IoT-dev
balena env add HOME           "/iot"                 --application IoT-dev
balena env add IOT            "/iot"                 --application IoT-dev
balena env add IOT49          "/iot/iot49"           --application IoT-dev
balena env add TZ             "America/Los_Angeles"  --application IoT-dev

balena env add JUPYTER_PORT   "8888"                 --application IoT-dev --service jupyter
balena env add JUPYTER_IP     "*"                    --application IoT-dev --service jupyter
balena env add JUPYTER_ALLOW_INSECURE_WRITES "true"  --application IoT-dev --service jupyter

balena env add SAMBA_SERVER   "no"                   --application IoT-dev
balena env add SAMBA_CLIENT   "yes"                  --application IoT-dev
balena env add SAMBA_IP       "10.39.40.151"         --application IoT-dev
balena env add SAMBA_PASSWORD "jhlkq3452344"         --application IoT-dev

# enable samba server on pi4server

balena env add SAMBA_SERVER   "yes"                  --device 200a469
balena env add SAMBA_CLIENT   "no"                   --device 200a469

# show current configuration

echo "Default Configuration"
balena envs --application IoT-dev

echo
echo "Server Configuration"
balena envs --device 200a469
