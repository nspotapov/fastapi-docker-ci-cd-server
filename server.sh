#!/usr/bin/env bash

if [ ! -d "cicdserver_venv" ]
then
  '/usr/bin/python3 -m venv cicdserver_venv'
fi

'bash cicdserver_venv/activate'
'pip3 install -r requirements.txt'

'uvicorn main:app'
