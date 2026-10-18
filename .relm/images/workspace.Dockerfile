# Relm workspace image for Saleor: the upstream devcontainer (.devcontainer/Dockerfile) plus the
# packages Relm's runtime contract needs (unzip, jq, libnsl2). Dependencies are installed
# system-wide, as in the devcontainer, so `pytest` and `./manage.py` run with no venv.
# Image spec user: vscode. Entrypoint: /usr/local/bin/entrypoint.sh
FROM --platform=linux/amd64 mcr.microsoft.com/devcontainers/python:3.12

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  libffi8 libgdk-pixbuf-2.0-0 liblcms2-2 libopenjp2-7 libssl3 libtiff6 libwebp7 libpq5 \
  shared-mime-info libmagic1 media-types \
  unzip jq libnsl2 postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.1@sha256:cf4eedcaa81655197f625739489effcbe71b61ceb1506f332c3facae5deceded \
  /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_SYSTEM_PYTHON=1 UV_PROJECT_ENVIRONMENT=/usr/local
COPY uv.lock pyproject.toml /tmp/saleor/
RUN cd /tmp/saleor && uv sync --locked --no-install-project --no-editable \
  && rm -rf /tmp/saleor /root/.cache/uv

# The base image's mypy clashes with the version in uv.lock (same as upstream)
RUN pipx uninstall mypy || true

RUN printf '#!/bin/sh\nexit 0\n' > /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh
