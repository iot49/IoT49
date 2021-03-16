#!/bin/bash

# install iot49 jupyter enviroment for MicroPython

sudo -s -- <<'EOF'
apt update
apt -y full-upgrade

apt -y install git
apt -y install python3-pip
apt -y install python3-venv
apt -y install direnv

apt -y install libxml2-dev libxslt-dev
apt -y install libblas-dev liblapack-dev
apt -y install libatlas-base-dev gfortran
apt -y install libtiff5-dev libjpeg62-turbo-dev
apt -y install zlib1g-dev libfreetype6-dev liblcms2-dev
apt -y install libwebp-dev tcl8.5-dev tk8.5-dev
apt -y install libharfbuzz-dev libfribidi-dev
apt -y install libhdf5-dev
apt -y install libnetcdf-dev
apt -y install libzmq3-dev
apt -y install pandoc
apt -y install texlive-xetex
apt -y install latexmk
apt -y install sqlite3
apt -y install dfu-util
apt -y install software-properties-common
apt -y install nodejs
apt -y install npm
apt -y install minicom
apt -y install gcc-arm-none-eabi
apt -y install libnewlib-arm-none-eabi
EOF

# install global gitignore

cp ~/iot49/pi/bin/gitignore_global ~/.gitignore_global


# enable .gitignore_global
git config --global core.excludesfile ~/.gitignore_global

######################################################################################
# setup a virtual environment based on direnv (https://direnv.net/)

sudo pip3 install virtualenv

# add direnv hook to bash shell
cat << 'EOF' >> ~/.bashrc

# direnv (https://direnv.net/)
cd ~
eval "$(direnv hook bash)"
EOF

source ~/.bashrc

# setup python virtual environment (https://direnv.net/man/direnv-stdlib.1.html)
echo "layout python3" >~/iot49/.envrc
cd ~/iot49
direnv allow

# activate virtual environment from script
eval "$(direnv export bash)"

# install requirements to virtual environment
pip3 install setuptools
pip3 install -U pip

cat ~/iot49/pi/bin/requirements.txt | xargs -n 1 pip3 install

# enable bluetooth access for the pi user
sudo usermod -a -G bluetooth $USER

######################################################################################
# configure the jupyter notebook server

# generated default jupyter config in ~/.jupyter
jupyter notebook -y --generate-config

# set up dictionary of changes
declare -A arr
app='c.ServerApp'
arr+=(["$app.open_browser"]="$app.open_browser = False")
arr+=(["$app.ip"]="$app.ip ='*'")
arr+=(["$app.port"]="$app.port = 8888")
arr+=(["c.NotebookApp.enable_mathjax"]="c.NotebookApp.enable_mathjax = True")
arr+=(["$app.root_dir"]="$app.root_dir = '/home/pi/iot49'")
arr+=(["$app.password"]="$app.password = 'sha1:5815fb7ca805:f09ed218dfcc908acb3e29c3b697079fea37486a'")
arr+=(["$app.allow_remote_access"]="$app.allow_remote_access = True")

# apply changes to jupyter_notebook_config.py

target=~/.jupyter/jupyter_notebook_config.py

for key in ${!arr[@]};do
    if grep -qF $key ${target}; then
        # key found -> replace line
        sed -i "/${key}/c ${arr[${key}]}" $target
    else
        # key not found -> append line
        echo "${arr[${key}]}" >> $target
    fi
done

# install the iot-kernel
python -m iot_kernel.install

######################################################################################
# create a service to start jupyter lab automatically

# startup script
cat << 'ONE' > /home/pi/start_jupyter.sh && chmod a+x /home/pi/start_jupyter.sh
#!/bin/bash
cd iot49

# activate virtual environment from script
eval "$(direnv export bash)"

# start server
jupyter lab
ONE

# setup the service
cat << 'TWO' | sudo tee /etc/systemd/system/jupyter.service
[Unit]
Description=Jupyter
[Service]
Type=simple
ExecStart=/home/pi/start_jupyter.sh
User=pi
Group=pi
WorkingDirectory=/home/pi/iot49
Environment="IOT=/home/pi"
Environment="IOT49=/home/pi/iot49"
Restart=always
RestartSec=10
[Install]
WantedBy=multi-user.target
TWO

# enable the service and start the jupyter server
sudo systemctl daemon-reload
sudo systemctl start jupyter
sudo systemctl enable jupyter
