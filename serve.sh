#!/bin/sh
# Serve the two HTML pages locally on http://localhost:8000
# Usage: ./serve.sh [port]
set -e
cd "$(dirname "$0")"
PORT="${1:-8000}"
( sleep 1 && open "http://localhost:${PORT}/" ) &
exec python3 -m http.server "${PORT}" --bind 127.0.0.1
