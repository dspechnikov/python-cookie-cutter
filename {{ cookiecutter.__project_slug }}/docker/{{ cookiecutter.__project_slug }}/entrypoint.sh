#!/usr/bin/env bash

{% if cookiecutter.database == 'Postgres' %}
# wait for database container to accept connections, because:
# - docker compose service_healthy condition causes docker compose run to fail
# - it's useful for isolated container runs without docker compose dependency management
wait-for-it \
  --host="${% raw %}{{% endraw %}{{ cookiecutter.__project_slug | upper }}_DATABASE_HOST}" \
  --port="${% raw %}{{% endraw %}{{ cookiecutter.__project_slug | upper }}_DATABASE_PORT:-5432}" \
  --timeout=30 \
  --strict
{%- endif %}

exec "$@"
