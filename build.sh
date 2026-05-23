#!/usr/bin/env bash
uv install --no-root

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install

chmod +x ./build.sh
