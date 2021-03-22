#!/bin/bash
# idf.py

# assumes we are in micropython/ports/XXX
mp_root="../.."
mpy_cross_dir="$mp_root/mpy-cross"
mpy_cross_name="ubuntu-mpy-cross"

# use custom image if on arm
# Note: check https://hub.docker.com/r/espressif/idf/tags for available versions (Tags)
image="espressif/idf:release-v4.2"
if [ "$(uname -m)" == "armv7l" ]; then
    image="esp-idf-arm7:v4.2"
fi

# build mpy-cross for Ubuntu
if [ ! -f "$mpy_cross_dir/$mpy_cross_name" ]; then
    echo building "$mpy_cross_dir/$mpy_cross_name"
    rm -rf "$mpy_cross_dir/build"
    docker run --rm \
        -v "$mp_dir":/mp -w /mp/mpy-cross \
        "$image" make PROG="$mpy_cross_name"
fi

# delegate idf.py to docker
# Note: set --device and/or --pivileged to enable flashing
docker run --rm \
    -e MICROPY_MPYCROSS="/mp/mpy-cross/$mpy_cross_name" \
    -v $(realpath "$mp_root"):/mp -w /mp/ports/esp32 \
    "$image" idf.py "$@"

# debugging helper ...
# bash propmt in the idf docker
# docker run -it -v $IOT/micropython:/mp -w /mp/ports/esp32 "espressif/idf:release-v4.2"
