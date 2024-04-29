# System libraries:
import os
import asyncio
import re

# Project libraries:
from lib.helpers import *
from lib.common import *
from lib.classes import Conversation

from munch import Munch
from munch import munchify
from markdown import markdown

from app import llm
from app import flask_app
from flask import render_template

@flask_app.get("/session/<session_name>")
def session_sn_GET(session_name):
    try:
        common = get_common_vars()
        common.session = None

        for s in common.sessions:
            if s.name == session_name:
                common.session = s

        if common.session is None:
            convo = Conversation(session_name, llm)
            common.session = get_conversation_var(convo)

        return render_template("session.html", common=common)
    except Exception as x:
        print(x)
        return ""

@flask_app.get("/sessions")
def sessions_GET():
    try:
        return render_template("sessions.html", common=get_common_vars())
    except Exception as x:
        print(x)
        return ""

@flask_app.template_global()
def md(f_path):
    try:
        f_text = read_file(f_path, "")
        f_markdown = markdown(f_text)
        return f_markdown
    except Exception as x:
        print(x)
        return str(x)
