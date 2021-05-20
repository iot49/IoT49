#!/bin/bash

# sensible default for $IOT49 if it's not defined
iot49=${IOT49:=${HOME}/iot49}

# dev: mount iot49-dev to iot49
mkdir -p $iot49
mount -t cifs //10.39.40.114/iot49-dev $iot49 \
    -osec=ntlmssp,domain=WORKGROUP,username=boser,password='m@ru$o5X',uid=$(id -u),gid=$(id -g)

# dev: mount iot-device
mkdir -p ${HOME}/iot-device
mount -t cifs //10.39.40.114/iot-device ${HOME}/iot-device \
    -osec=ntlmssp,domain=WORKGROUP,username=boser,password='m@ru$o5X',uid=$(id -u),gid=$(id -g)

# dev: mount iot-kernel
mkdir -p ${HOME}/iot-kernel
mount -t cifs //10.39.40.114/iot-kernel ${HOME}/iot-kernel \
    -osec=ntlmssp,domain=WORKGROUP,username=boser,password='m@ru$o5X',uid=$(id -u),gid=$(id -g)

# start shutdown monitor (MOTOR_HAT)
monitor=$iot49/projects/robot/shutdown_monitor.py
if [ -f $monitor ]; then
    python $monitor &
fi

# start jupyter lab server
jupyter lab --allow-root --ip=${JUPYTER_IP:=*} --port=${JUPYTER_PORT:=8888} --no-browser
