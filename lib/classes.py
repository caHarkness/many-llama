import re
import json

import lib.helpers
from lib.helpers import *

class Conversation:
    def __init__(self, session_name, llm):
        self.session = {}
        self.session_name = session_name
        self.session_path = f"sessions/{session_name}.json"
        self.llm = llm

        # Automatically load on instantiation:
        self.load()

    def load(self, last_n_messages=None):
        f_text = read_file(self.session_path, "{}")
        f_json = json.loads(f_text)
        self.session = f_json

        self.session["user_name"] = safely_get(self.session, "user_name", DEFAULT_USER_NAME)
        self.session["assistant_name"] = safely_get(self.session, "assistant_name", DEFAULT_ASSISTANT_NAME)

        user_name = self.session["user_name"]
        assistant_name = self.session["assistant_name"]

        default_context = DEFAULT_CONTEXT.format(
            user_name=user_name,
            assistant_name=assistant_name)

        self.session["context"] = safely_get(self.session, "context", default_context)
        self.session["conversation"] = safely_get(self.session, "conversation", [])

        self.user_name = user_name
        self.assistant_name = assistant_name

        if last_n_messages is not None:
            while len(self.session["conversation"]) > last_n_messages:
                self.session["conversation"].pop(0)
            self.index_messages()

    def save(self, complete=False):
        self.index_messages()

        f_text = json.dumps(self.session, indent=4)
        write_file(self.session_path, f_text)

        if complete == True:
            timestamp = get_timestamp(fname_safe=True)
            write_file(f"scripts/{self.session_name}_{timestamp}.txt", self.get_chat_text())


    def get_chat_text(self):
        output = ""
        for o in self.session["conversation"]:
            name = o["name"]
            message = o["message"]
            output += f"<{name}>: {message}\n\n"

        output = output.rstrip()
        output += "\n"
        return output

    # The following template comes from:
    # https://huggingface.co/TheBloke/dolphin-2.1-mistral-7B-GGUF
    def build_prompt_chatml(self, user_input):
        context = self.session["context"]
        output = f"<|im_start|>system\n{context}<|im_end|>\n"


        for o in self.session["conversation"]:
            name = o["name"]
            message = o["message"]

            name = "user" if name == self.user_name else name
            name = "assistant" if name == self.assistant_name else name

            output += f"<|im_start|>{name}\n{message}<|im_end|>\n"


        output += f"<|im_start|>assistant"
        return output

    def get_conversation(self):
        return self.session["conversation"]

    def index_messages(self):
        for i in range(0, len(self.session["conversation"])):
            o = self.session["conversation"][i]
            o["order"] = i
            self.session["conversation"][i] = o

    def add_message(self, name, message):
        self.index_messages()

        current_index = len(self.session["conversation"])

        self.session["conversation"].append({
            "order": current_index,
            "name": name,
            "message": message,
            "time": get_timestamp(),
            "type": "query" if name == self.user_name else "reply"
        })

    def get_response(self, user_input):

        output = ""
        generation = self.llm(
            self.build_prompt_chatml(user_input),
            max_tokens=12288,
            stop=["<|im_end|>"],
            echo=False,
            repeat_penalty=1.1,
            temperature=0.75
        )

        if "choices" in generation:
            if len(generation["choices"]) > 0:
                output = generation["choices"][0]["text"].strip()

        return output
