from lib.classes import *
from llama_cpp import Llama

# Load the LLM model:
llm = Llama(
    model_path="models/TheBloke/dolphin-2.6-mistral-7B-GGUF/dolphin-2.6-mistral-7b.Q4_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=16384
)

# See lib/classes.py:
convo = Conversation("default", llm)

while True:
    print("")
    query = input("> ")
    convo.add_message(convo.session.user_name, query)

    reply = convo.get_reply()
    convo.add_message(convo.session.assistant_name, reply)

    print("")
    print(reply)
