#!/usr/bin/env bash

if [ ! -d "venv" ]
then
  python3 -m venv venv
fi

bash cicdserver_venv/activate
pip3 install -r requirements.txt

uvicorn main:app
