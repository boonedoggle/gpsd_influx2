#!/usr/bin/env bash
set -e # Forces exit on errors

CURRENT_DIR=$(pwd)
INSTALL_DIR="/opt/gpsd_influx2"
SERVICES_DIR="/etc/systemd/system"

# Make sure you are sudo
if [ "$(id -u)" -ne "0" ] ; then
    echo "This script must be executed with root privileges. Exiting Now."
    exit 1
fi

# Copy files
mkdir $INSTALL_DIR
cp gpsd_influx2.sh "$INSTALL_DIR/gpsd_influx2.py"
cp config.ini.sample "$INSTALL_DIR/config.ini.sample"
cp config.ini.sample "$INSTALL_DIR/config.ini"
cp uninstall.sh "$INSTALL_DIR/uninstall.sh"
cp gpsd_influx2.service "$SERVICES_DIR/gpsd_influx2.service"

# Make executable
chmod +x "$INSTALL_DIR/gpsd_influx2.py"

# Create venv
cd "$INSTALL_DIR"
virtualenv venv --python=python3
source "$INSTALL_DIR/venv/bin/activate"
pip install -r requirements.txt
deactivate
cd "$CURRENT_DIR"

# Reload system services
systemctl daemon-reload

echo "Edit $INSTALL_DIR/config.ini with your InfluxDB settings."