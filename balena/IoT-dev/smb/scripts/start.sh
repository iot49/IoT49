#!/bin/bash

function setup_user {
  SMB_USER=root
  SMB_PASS=${SAMBA_PASSWORD:=iot49}
  usermod -aG smbgroup $SMB_USER
  printf "${SMB_PASS}\n${SMB_PASS}\n" | smbpasswd -a -s $SMB_USER
  smbpasswd -e $SMB_USER
}

function main {
  if [ "$SAMBA_SERVER" == yes ]
  then
    echo "Start samba server"
    cat ${CONFIG_DIR}/smb.conf > /etc/samba/smb.conf
    setup_user
    smbd $@
  else
    echo "Samba server disabled"
    while : ;
    do
      echo 'Idling...'
      sleep 600
    done
  fi
}

main $@
