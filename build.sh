#!/usr/bin/env bash
set -o errexit

curl -LsSf https://astral.sh/install.sh | sh
source $HOME/.local/bin/env

make install
