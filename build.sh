#!/usr/bin/env bash
set -o errexit

poetry install --no-interaction --no-root

psql -a -d "$DATABASE_URL" -f database.sql
