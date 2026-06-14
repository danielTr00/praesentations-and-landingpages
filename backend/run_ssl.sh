#!/bin/bash
cd "$(dirname "$0")"
echo "Starting CLG Backend with HTTPS..."
echo "SSL Endpoint: https://192.168.178.87.sslip.io:8443"
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8443 \
    --ssl-keyfile certs/server.key \
    --ssl-certfile certs/server.crt \
    --log-level info
