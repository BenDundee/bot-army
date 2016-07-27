#!
#!/usr/bin/bash
#-x
. $rightImportCyg/bashrc_automation.sh # error handling logic

## Step 0: Make sure pip and virtualenv are installed
cd /tmp
wget https://bootstrap.pypa.io/get-pip.py
python3.5 /tmp/get-pip.py
pip3.5 install virtualenv

## Cleanup
rm *get-pip.py*

## Place where environment lives

# INSTALL_DIR=/

## Step 1: build the virtualenv
virtualenv $INSTALL_DIR --no-site-packages -p /usr/bin/python3.5
