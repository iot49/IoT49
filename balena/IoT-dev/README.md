# IoT-dev

MicroPython development environment as a balena app.


## Services

* Samba Mount: if SAMBA_CLIENT=yes

| Service   | Samba Mount  | Comments                   |
|-----------|--------------|----------------------------|
| jupyter   | yes          | start-jupyter.sh           |
| vsc       | yes          |                            |
| gcc       | yes          |                            |
| duplicati | no           | auto-mount usb drives      |
| smb       | no           | start if SAMBA_SERVER=yes  |
