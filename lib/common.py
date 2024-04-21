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
from munch import Munch
from munch import munchify

def get_conversation_var(convo):
    so = munchify(convo.session)

    so.last_message = convo.get_last_message()
    if so.last_message is not None:
        so.last_message = munchify(so.last_message)
        if len(so.last_message.body) > 50:
            so.last_message.body = so.last_message.body[:50].strip() + "..."

    so.has_hidden_messages = False
    for m in convo.get_messages():
        if "hidden" in m:
            if m.hidden == True:
                so.has_hidden_messages = True

    so.thread_name = so.name
    if so.display_as_contact:
        so.thread_name = so.assistant_name

    return so

def get_common_vars():
    common = Munch()
    common.session = "default"
    common.sessions = []

    sessions = []
    if os.path.isdir("sessions"):
        for s in os.listdir("sessions"):
            if re.match(r"^_", s):
                continue

            session_name    = re.search(r"(.+)\.json$", s).group(1)
            convo           = Conversation(session_name)
            so              = get_conversation_var(convo)
            sessions.append(so)

    sessions.sort(key=lambda x: x.last_message.time if x.last_message is not None else x.name, reverse=True)

    common.sessions = sessions
    common.session_name_regex = "^[A-Za-z0-9_\\-]{1,}$"

    return common
