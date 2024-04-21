# System libraries:
import os
import asyncio
import re

# Project libraries:
from lib.helpers import *
from lib.classes import Conversation

# Pip libraries:
from llama_cpp import Llama
from flask import Flask

# Load the LLM model:
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1,
    n_ctx=16384
)

# Prepare the Flask app:
flask_app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
flask_app.config["TEMPLATES_AUTO_RELOAD"] = True

# Load the Flask routing:
from lib.redirects import *
from lib.views import *
from lib.v1 import *
