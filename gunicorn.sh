#! /bin/bash

gunicorn -D -b unix:./gun_fmpusher.sock -w 2 -p ./gun_fmpusher.pid FMPusher.wsgi
