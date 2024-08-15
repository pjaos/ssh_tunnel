#!/bin/bash
set -e
pyflakes3 server/*.py
pyflakes3 server_lib/*.py
pyflakes3 mcu/*.py

