FROM docker.io/python:3.12.2-slim-bookworm AS python

# Stage 1: Build our dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=production

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r ${BUILD_ENVIRONMENT}.txt

# Stage 2: Python run stage.
FROM python AS python-run-stage
ARG BUILD_ENVIRONMENT=production

ARG APP_HOME=/app

# Reduce space usage by avoiding __pycache__/ files
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \  
  sudo git bash-completion nano ssh

# Creating new system user avoiding default docker root priviledges
RUN addgroup --system django && \
  adduser --system --ingroup django django && \
  mkdir -p ${APP_HOME}/staticfiles && \
  chown django:django ${APP_HOME}/staticfiles && \
  chmod 775 ${APP_HOME}/staticfiles

# Install additional runtime dependencies and clean up apt cache
RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy pre-built wheels from build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install Python packages from wheels and clean up
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy and configure Django entrypoint script
COPY --chown=django:django ./docker/production/django/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint  # Remove Windows line endings
RUN chmod +x /entrypoint           # Make script executable

# Copy and configure Django start script
COPY --chown=django:django ./docker/production/django/start.sh /start
RUN sed -i 's/\r$//g' /start      # Remove Windows line endings
RUN chmod +x /start               # Make script executable

# Copy and configure Celery worker start script
COPY --chown=django:django ./docker/production/django/celery/worker/start.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

# Copy and configure Celery beat start script
COPY --chown=django:django ./docker/production/django/celery/beat/start.sh /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

# Copy and configure Celery flower start script
COPY --chown=django:django ./docker/production/django/celery/flower/start.sh /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# Copy project files and set ownership
COPY --chown=django:django . ${APP_HOME}

# Ensure proper ownership of application directory
RUN chown django:django ${APP_HOME}

# Switch to non-root user
USER django

# Set the entrypoint script
ENTRYPOINT [ "/entrypoint" ]
