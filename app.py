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
from pathlib import Path

# Required dirs:
Path("./sessions").mkdir(parents=True, exist_ok=True)

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
    common["session"] = "default"
    common["sessions"] = []

    sessions = []
    for s in os.listdir("sessions"):
        if re.match(r"^_", s):
            continue

        sessions.append(re.search(r"(.+)\.json$", s).group(1))

    common["sessions"] = sessions
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
    return redirect("/session/default")

@app.get("/new")
def new_GET():
    md5_hash = new_md5()
    return redirect(f"/session/_{md5_hash}")

@app.get("/session/<sn>")
def session_sn_GET(sn):
    try:
        common = get_common_vars()
        common.session = sn
        return render_template("index.html", common=common)
    except:
        return ""

@app.post("/session/<sn>")
async def session_sn_POST(sn):
    query = None
    reply = None

    try:
        await thread_lock()
        global llm

        o = request.json
        query = o["query"]

        convo = Conversation(sn, llm)
        convo.load()
        convo.add_message(convo.user_name, query)
        reply = convo.get_response(query)
        convo.add_message(convo.assistant_name, reply)
        convo.save()

        print(f"QUERY: {query}")
        print(f"REPLY: {reply}")
    except:
        pass

    thread_unlock()
    return {
        "query": query,
        "reply": reply
    }

@app.get("/session/<sn>/messages")
async def session_sn_messages_GET(sn):
    try:
        await thread_lock()
        global llm
        convo = Conversation(sn, llm)
        convo.load()
        thread_unlock()
        return convo.session["conversation"]
    except:
        return []

@app.post("/session/<sn>/clear")
async def session_sn_clear_POST(sn):
    try:
        await thread_lock()
        global llm
        convo = Conversation(sn, llm)
        convo.load(0)
        convo.save()
    except:
        pass

    thread_unlock()
    return { "success": True }

@app.post("/session/<sn>/delete")
async def session_sn_delete_POST(sn):
    try:
        await session_sn_clear_POST(sn)
        await thread_lock()
        os.unlink(f"sessions/{sn}.json")
    except:
        pass
    
    thread_unlock()
    return { "success": True }

@app.get("/session/<sn>/rename/<nn>")
async def session_sn_rename_nn_GET(sn, nn):
    try:
        await thread_lock()
        f_data = read_file(f"sessions/{sn}.json", "")
        write_file(f"sessions/{nn}.json", f_data)
        os.unlink(f"sessions/{sn}.json")
    except:
        pass

    thread_unlock()
    return redirect(f"/session/{nn}")
