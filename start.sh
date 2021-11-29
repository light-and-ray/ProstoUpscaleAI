#!/bin/bash
CURRENT_FILE_DIR=`dirname "${BASH_SOURCE[0]}"`
cd "$CURRENT_FILE_DIR/src"
exec python3 main.py
