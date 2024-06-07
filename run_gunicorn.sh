#!/bin/bash
source ~/voxvideos.rubenmaestre.com/venv/bin/activate
nohup gunicorn -k eventlet -w 1 -b :8002 app:app > gunicorn.log 2>&1 &

