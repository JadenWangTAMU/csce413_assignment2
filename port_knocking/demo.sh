#!/usr/bin/env bash

set -euo pipefail

TARGET_IP=${1:-127.0.0.1}
SEQUENCE=${2:-"1560,6580,8153"}
PROTECTED_PORT=${3:-2222}

echo "[1/3] Attempting protected port before knocking"
nc -z -v "$TARGET_IP" "$PROTECTED_PORT" || true

echo "[2/3] Sending knock sequence: $SEQUENCE"
python3 knock_client.py --target "$TARGET_IP" --sequence "$SEQUENCE" --check

echo "[3/3] Attempting protected port after knocking"
nc -z -v "$TARGET_IP" "$PROTECTED_PORT" || true

