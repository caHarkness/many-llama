import re
import json
import os

import lib.helpers
from lib.helpers import *

class Conversation:
    def __init__(self, session_name, llm=None):
        self.session = {}
        self.rename(session_name)
        self.llm = llm

        # Automatically load on instantiation:
        self.load()

    def rename(self, new_session_name):
        old_session_name = None
        if hasattr(self, "session_name"):
            old_session_name = self.session_name

        self.session_name = new_session_name
        self.session_path = f"sessions/{new_session_name}.json"

        try:
            if old_session_name is not None:
                os.unlink(f"sessions/{old_session_name}.json")
        except:
            pass

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
            # If the number is 0 or positive, use that many messages from the end of the list:
            if last_n_messages > -1:
                while len(self.session["conversation"]) > last_n_messages:
                    self.session["conversation"].pop(0)

            # If the number is negative, use that many messages from the top:
            if last_n_messages < 0:
                last_n_messages = abs(last_n_messages)
                while len(self.session["conversation"]) > last_n_messages:
                    arr_len = len(self.session["conversation"])
                    self.session["conversation"].pop(arr_len - 1)

            self.index_messages()



    def save(self, complete=False):
        self.index_messages()

        f_text = json.dumps(self.session, indent=4)
        write_file(self.session_path, f_text)

        if complete == True:
            timestamp = get_timestamp(fname_safe=True)
            write_file(f"scripts/{self.session_name}_{timestamp}.txt", self.get_chat_text())

    def delete(self):
        try:
            session_name = self.session_name
            os.unlink(f"sessions/{session_name}.json")
        except:
            pass


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
        if self.llm is None:
            raise Exception("Conversation LLM is None")

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

    def get_last_message(self):
        conversation = self.session["conversation"]
        message = conversation[len(conversation) - 1]
        return message

