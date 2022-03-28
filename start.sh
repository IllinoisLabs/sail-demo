#!/usr/bin/env bash

# install packages
python3 -m pip install -r requirements.txt

# run flask server
python3 backend/api.py &

# make browser request to web server before server starts
open http://localhost:8000

# start web server
cd ./frontend && python3 -m http.server 8000

# on script terminate, kill processes that were started
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT