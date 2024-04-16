# System libraries:
import os
import asyncio
import re

# Project libraries:
from lib.helpers import *
from lib.classes import Conversation

# Pip libraries:
from llama_cpp import Llama
from munch import Munch
from munch import munchify

# Load the LLM model:
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1,
    n_ctx=16384
)

'''
Threading related:
'''
LOCK = False
async def thread_lock():
    global LOCK
    while LOCK is True:
        await asyncio.sleep(1)
    LOCK = True

def thread_unlock():
    global LOCK
    LOCK = False

'''
Common vars, i.e. the viewbag:
'''
def get_common_vars():
    common = Munch()
    common.session = "default"
    common.sessions = []

    sessions = []
    if os.path.isdir("sessions"):
        for s in os.listdir("sessions"):
            if re.match(r"^_", s):
                continue

            session_object = Munch()
            session_object.name = re.search(r"(.+)\.json$", s).group(1)
            session_object.last_message = {}

            convo = Conversation(session_object.name)
            last_message = convo.get_last_message()
            last_message = munchify(last_message)

            if len(last_message.message) > 50:
                last_message.message = last_message.message[:50].strip() + "..."

            session_object.last_message = last_message


            sessions.append(session_object)

    sessions.sort(key=lambda x: x.last_message.time, reverse=True)

    common.sessions = sessions
    common.session_name_regex = "^[A-Za-z0-9_\\-]{1,}$"
    return common

'''
Flask Routing:
'''
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def main():
    return redirect("/sessions")

@app.get("/new")
def new_GET():
    md5_hash = new_md5()
    return redirect(f"/session/_{md5_hash}")

@app.get("/session/<sn>")
def session_sn_GET(sn):
    try:
        common = get_common_vars()
        common.session = sn
        return render_template("session.html", common=common)
    except:
        return ""

@app.get("/sessions")
def sessions_GET():
    try:
        return render_template("sessions.html", common=get_common_vars())
    except:
        return ""

@app.post("/v1")
async def v1_POST():
    try:
        await thread_lock()
        global llm

        o = request.json
        convo = Conversation(o["session"], llm)

        last_n_messages = None

        if "last_n_messages" in o:
            last_n_messages = int(o["last_n_messages"])

        if "clear_session" in o:
            if o["clear_session"] == 1:
                last_n_messages = 0

        convo.load(last_n_messages)

        if last_n_messages == 0:
            if "context" in o:
                convo.add_message(convo.user_name, o["context"])

        query = o["input"]
        convo.add_message(convo.user_name, query)
        reply = convo.get_response(query)
        convo.add_message(convo.assistant_name, reply)
        convo.save()

        thread_unlock()
        return { "output": reply }
    except:
        pass

    thread_unlock()
    return { "output": "Error" }


@app.get("/v1/session/<session_name>")
async def v1_session_sn_GET(session_name):
    try:
        await thread_lock()
        global llm

        convo = Conversation(session_name, llm)
        convo.load()
        thread_unlock()

        return convo.session
    except:
        thread_unlock()
        return ""

@app.post("/v1/session/<session_name>")
async def v1_session_sn_POST(session_name):
    try:
        await thread_lock()
        global llm

        o = request.json
        convo = Conversation(session_name, llm)

        last_n_messages = None

        if "last_n_messages" in o:
            last_n_messages = int(o["last_n_messages"])

        if "clear_session" in o:
            if o["clear_session"] == 1:
                last_n_messages = 0

        convo.load(last_n_messages)

        if last_n_messages == 0:
            if "context" in o:
                convo.add_message(convo.user_name, o["context"])

        query = o["query"]
        convo.add_message(convo.user_name, query)
        reply = convo.get_response(query)
        convo.add_message(convo.assistant_name, reply)
        convo.save()

        thread_unlock()
        return { "reply": reply }
    except Exception as x:
        print(x)
        pass

    thread_unlock()
    return { "reply": "Error" }

@app.post("/v1/session/<session_name>/rename")
async def v1_session_sn_rename_POST(session_name):
    try:
        await thread_lock()
        global llm

        o = request.json
        new_session_name = o["new_session_name"]
        convo = Conversation(session_name, llm)
        convo.load()
        convo.rename(new_session_name)
        convo.save()

        thread_unlock()
        return { "session_name": new_session_name }
    except Exception as x:
        print(x)
        pass

    thread_unlock()
    return { "session_name": session_name }

@app.post("/v1/session/<session_name>/delete")
async def v1_session_sn_delete_POST(session_name):
    try:
        await thread_lock()
        global llm

        o = request.json
        session_name = o["session_name"]

        convo = Conversation(session_name, llm)
        
        if session_name != convo.session_name:
            raise Exception()

        convo.delete()

        thread_unlock()
        return { "deleted": True }
    except:
        pass

    thread_unlock()
    return { "deleted": False }
