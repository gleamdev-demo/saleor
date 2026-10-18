# Relm workspace image for Saleor: the upstream devcontainer (.devcontainer/Dockerfile) plus the
# packages Relm's runtime contract needs (unzip, jq, libnsl2). Dependencies are installed
# system-wide, as in the devcontainer, so `pytest` and `./manage.py` run with no venv.
# Image spec user: vscode. Entrypoint: /usr/local/bin/entrypoint.sh
# Pinned to bookworm: Relm's bundled sshd is built against OpenSSL 3.0; the default (trixie) tag ships
# OpenSSL 3.5 and sshd exits at start ("OpenSSL version mismatch"), leaving the workspace without SSH.
FROM --platform=linux/amd64 mcr.microsoft.com/devcontainers/python:3.12-bookworm

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

# GitHub CLI, so the agent can open pull requests (the platform default image ships it)
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    > /etc/apt/sources.list.d/github-cli.list \
  && apt-get update && apt-get install -y --no-install-recommends gh \
  && rm -rf /var/lib/apt/lists/*

# The base image's mypy clashes with the version in uv.lock (same as upstream)
RUN pipx uninstall mypy || true

RUN printf '#!/bin/sh\nexit 0\n' > /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh
