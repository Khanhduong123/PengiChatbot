#!/usr/bin/env bash
PORT="${PORT:-9999}"
HOST="${HOST:-0.0.0.0}"

uvicorn main:app --host $HOST --port $PORT --forwarded-allow-ips '*' --reload