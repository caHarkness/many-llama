#!/bin/bash

# The directory to store the models:
export MODEL_DIR="models"

# The Hugging Face repository of the GGUF model:
export MODEL_REPO="TheBloke/dolphin-2.6-mistral-7B-GGUF"

# The specific GGUF file name of the model from the repository to be used:
export MODEL_GGUF="dolphin-2.6-mistral-7b.Q4_K_M.gguf"

# The entire path:
export MODEL_PATH="${MODEL_DIR}/${MODEL_REPO}/${MODEL_GGUF}"

# The name of the user providing the input:
export DEFAULT_USER_NAME="User"

# The name of the assistant providing responses:
export DEFAULT_ASSISTANT_NAME="Assistant"

# The context of the conversation:
# NOTE: use {user_name} and {bot_name} where the names need to be substituted
export DEFAULT_CONTEXT="This is a conversation between a user named {user_name} and another user named {assistant_name}. {assistant_name} is short, stern, and straight to the point. {assistant_name} is almost impolite and seemingly uninterested, but will have a change of attitude if {user_name} asks. If {assistant_name} is not 100 percent confident of its answer, it will reply stating it does not know and will not try to guess the answer."
