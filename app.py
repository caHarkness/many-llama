import os
from lib.helpers import *
from lib.classes import Conversation
from llama_cpp import Llama

llm = Llama(
    model_path="models/TheBloke/dolphin-2.6-mistral-7B-GGUF/dolphin-2.6-mistral-7b.Q4_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=16384
)

if __name__ == "__main__":

    convo = Conversation("default", llm)
    convo.load()

    while True:
        try:
            os.system("clear")

            if len(convo.get_conversation()) > 0:
                print(convo.get_chat_text())

            user_input = input(f"<{convo.user_name}>: ")
            convo.add_message(convo.user_name, user_input)

            response = convo.get_response(user_input)

            convo.add_message(convo.bot_name, response)
            convo.save()
        except KeyboardInterrupt as ki:
            break

    os.system("clear")
    convo.save(True)
    print("Saved")
