#!/bin/sh

cd /opt/amocrm/asterisk/bin

if [ -f "app.pid" ]
then
    PID=$(cat "app.pid")
    if ps -p $PID > /dev/null
    then
	echo "$PID is running"
	exit
    fi
    rm app.pid
fi

. venv/bin/activate
python ./app.py
