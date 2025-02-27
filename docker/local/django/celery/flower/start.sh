#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -o errexit
# Exit if any unset variables are used
set -o nounset

# Start Flower monitoring tool with auto-reload using watchfiles
# --filter python: Only watch Python files
# celery.__main__.main: Entry point for Celery
# -A config.celery_app: Specify the Celery app to use
# -b: Broker URL from environment variable
# flower: Run Flower monitoring interface
# --basic_auth: Set authentication credentials from environment variables
exec watchfiles --filter python celery.__main__.main \
  --args \
  "-A config.celery_app -b \"${CELERY_BROKER_URL}\" flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""
