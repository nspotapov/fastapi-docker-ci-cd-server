#!/usr/bin/env bash

# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs -d '\n')

uvicorn main:app --host $DEPLOY_HOST --port $DEPLOY_PORT
