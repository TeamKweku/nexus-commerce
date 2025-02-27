#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -o errexit
# Exit if any unset variables are used
set -o nounset

# Remove any existing PID file to prevent startup issues
rm -f './celerybeat.pid'

# Start Celery beat with auto-reload using watchfiles
# --filter python: Only watch Python files
# celery.__main__.main: Entry point for Celery
# -A config.celery_app: Specify the Celery app to use
# beat: Run as a scheduler
# -l INFO: Set logging level to INFO
exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'
