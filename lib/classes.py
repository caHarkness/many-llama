import re
import json
import os
import copy

import lib.helpers
from lib.helpers import *

from munch import Munch
from munch import munchify

class Conversation:
    def __init__(self, session_name, llm=None):
        self.session        = Munch()
        self.session.name   = session_name
        self.llm            = llm

        # Automatically load on instantiation:
        self.load()

    def session_set(self, key, value):
        self.session[key] = value

    def get_file_path(self, session_name=None):
        if session_name is None:
            session_name = self.session.name
        return f"sessions/{session_name}.json"

    def load(self, last_n_messages=None):
        current_name = self.session.name

        f_text = read_file(self.get_file_path(), "{}")
        f_json = json.loads(f_text)
        self.session = f_json
        self.session = munchify(self.session)

        self.session.name               = current_name
        self.session.user_name          = safely_get(self.session, "user_name", DEFAULT_USER_NAME)
        self.session.assistant_name     = safely_get(self.session, "assistant_name", DEFAULT_ASSISTANT_NAME)
        self.session.context            = safely_get(self.session, "context", DEFAULT_CONTEXT)
        self.session.last_n_messages    = safely_get(self.session, "last_n_messages", None)
        self.session.locked             = safely_get(self.session, "locked", False)
        self.session.display_as_contact = safely_get(self.session, "display_as_contact", False)
        self.session.messages           = safely_get(self.session, "messages", [])

        if last_n_messages is not None:
            # If the number is 0 or positive, use that many messages from the end of the list:
            if last_n_messages > -1:
                while len(self.session.messages) > last_n_messages:
                    self.session.messages.pop(0)

            # If the number is negative, use that many messages from the top:
            if last_n_messages < 0:
                last_n_messages = abs(last_n_messages)
                while len(self.session.messages) > last_n_messages:
                    arr_len = len(self.session.messages)
                    self.session.messages.pop(arr_len - 1)

    def get_messages(self):
        output = []

        for m_template in self.session.messages:
            m = copy.copy(m_template)
            m = munchify(m)

            m.author_name = None
            m.author_name = self.session.user_name      if m.author == "user"       else m.author_name
            m.author_name = self.session.assistant_name if m.author == "assistant"  else m.author_name

            m.type = None
            m.type = "query" if m.author == "user"      else m.type
            m.type = "reply" if m.author == "assistant" else m.type

            output.append(m)

        return output

    def get_next_message_id(self):
        m_id = 0
        for m in self.get_messages():
            if "id" in m:
                if isinstance(m.id, int):
                    m_id = m.id if m.id > m_id else m_id

        m_id += 1
        return m_id

    def save(self, new_session_name=None):
        f_text = json.dumps(self.session, indent=4)
        write_file(self.get_file_path(new_session_name), f_text)

    def delete(self):
        try:
            # Exit early if locked:
            if "locked" in self.session:
                if self.session.locked == True:
                    return

            os.unlink(self.get_file_path())
        except:
            pass

    def get_formatted_context(self):
        ctx = self.session.context
        ctx = ctx.format(
            user_name       = self.session.user_name,
            assistant_name  = self.session.assistant_name)
        return ctx

    # The following template comes from:
    # https://huggingface.co/TheBloke/dolphin-2.1-mistral-7B-GGUF
    def build_prompt_chatml(self, user_input):
        context = self.get_formatted_context()
        output = f"<|im_start|>system\n{context}<|im_end|>\n"

        for m in self.get_messages():
            output += f"<|im_start|>{m.author}\n{m.body}<|im_end|>\n"

        output += f"<|im_start|>assistant"
        return output

    def add_message(self, author, body):
        if author not in [self.session.user_name, self.session.assistant_name, "user", "assistant"]:
            raise Exception("Supplied name not in list of acceptable values")

        author = "user" if author == self.session.user_name else author
        author = "assistant" if author == self.session.assistant_name else author

        self.session.messages.append({
            "id": self.get_next_message_id(),
            "author": author,
            "body": body,
            "time": get_timestamp(),
            "hidden": False
        })

        return self.get_last_message()

    def get_last_message(self):
        messages = self.get_messages()
        message = None
        if len(messages) > 0:
            message = messages[-1]
        return message

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
