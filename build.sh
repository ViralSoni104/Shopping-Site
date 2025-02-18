#!/bin/bash
apt-get update
apt-get install -y libmysqlclient-dev
python3 -m venv /opt/venv
. /opt/venv/bin/activate
pip install -r requirements.txt
