#!/bin/bash
CURRENT_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
cd "$CURRENT_FILE_DIR/src"
exec python3 main.py
