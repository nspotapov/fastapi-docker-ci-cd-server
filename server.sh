#!/usr/bin/env bash

uvicorn main:app --host $DEPLOY_HOST --port $DEPLOY_PORT
