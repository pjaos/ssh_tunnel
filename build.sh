#!/bin/bash
set -e
rm -rf dist
./check_code.sh
poetry -vvv build
