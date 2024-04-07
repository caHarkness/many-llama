#!/bin/bash

# https://stackoverflow.com/a/1482133
SCRIPT_DIR="$(dirname -- "$(readlink -f -- "$0";)";)"
cd "$SCRIPT_DIR"

VENV_FOUND=""

# Activate the Python virtual environment:
# For Linux-made virtual environments with "bin" directory:
if [[ -e "./venv/bin/activate" ]]
then
    source ./venv/bin/activate
    VENV_FOUND=1
fi

# For Windows-made virtual environments with "Scripts" directory:
if [[ -e "./venv/Scripts/activate" ]]
then
    source ./venv/Scripts/activate
    VENV_FOUND=1
fi

if [[ -z "${VENV_FOUND}" ]]
then
    echo "No virtual environment found. Exiting..."
    exit
fi

# Load the user settings and configuration:
source ./config.sh

# Download the model if not present:
if [[ ! -e "${MODEL_PATH}" ]]
then
    mkdir -p "${MODEL_DIR}/${MODEL_REPO}"
    huggingface-cli download "${MODEL_REPO}" $MODEL_GGUF --local-dir "${MODEL_DIR}/${MODEL_REPO}" --local-dir-use-symlinks False
fi

# Run the Python script:
python -u app.py
