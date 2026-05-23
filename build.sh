#!/usr/bin/env bash
poetry install --no-root

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
poetry install
