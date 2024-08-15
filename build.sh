#!/bin/bash
set -e
rm -rf dist
./check_code.sh
poetry -vvv build

REM To install with pipx
REM python -m pipx ensurepath
REM python -m pipx install dist/ssh_tunnel-0.1.0-py3-none-any.whl