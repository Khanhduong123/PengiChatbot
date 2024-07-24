#!/usr/bin/env bash
PORT="${PORT:-8080}"
uvicorn 'main:app --port '8080' --host '0.0.0.0' --forwarded-allow-ips '*' --reload'