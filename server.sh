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

grep -v '^#' requirements.txt | xargs -n 1 pip3 install

# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs -d '\n')

gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind ${DEPLOY_HOST}:${DEPLOY_PORT}