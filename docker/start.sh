#!/bin/bash

# Jesus christ i hate this thing
# Source nvm and activate Node.js 24
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 24

# Activate Python virtual environment
source /opt/venv/bin/activate

# Run the build script
exec python build.py
