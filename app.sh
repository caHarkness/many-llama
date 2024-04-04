#!/bin/bash

# https://stackoverflow.com/a/1482133
SCRIPT_DIR="$(dirname -- "$(readlink -f -- "$0";)";)"
cd "$SCRIPT_DIR"

# Activate the Python virtual environment:
source ./venv/bin/activate

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
