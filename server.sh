#!/usr/bin/env bash

if [ ! -d "/venv/" ]
then
  python3 -m venv venv
fi

cd venv
cd bin

chmod a+x activate
source activate

cd ..
cd ..

pip3 install -r requirements.txt

# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs -d '\n')

# uvicorn main:app --host $DEPLOY_HOST --port $DEPLOY_PORT
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind ${DEPLOY_HOST}:${DEPLOY_PORT}