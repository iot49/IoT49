#!/bin/bash
# idf.py

# we assume we are in ports/esp32
mp_root="../.."
mpy_cross="mpy-cross-ubuntu"

# build mpy-cross for Ubuntu
if [ ! -f "$mp_root/mpy-cross/$mpy_cross" ]; then
    echo building "$mp_root/mpy-cross/$mpy_cross"
    cd "$mp_root/mpy-cross"
    make PROG="$mpy_cross"
    cd -
fi

# and use it
export MICROPY_MPYCROSS="$mp_root/mpy-cross/$mpy_cross"

# delegate idf.py to docker
# Note 1: check https://hub.docker.com/r/espressif/idf/tags for available versions (Tags)
# Note 2: also set --device and/or --pivileged to enable flashing
docker run --rm -v $(realpath "$mp_root"):/mp -w /mp/ports/esp32 "espressif/idf:release-v4.2" idf.py "$@"
