# System libraries:
import os
import asyncio
import re

# Project libraries:
from lib.helpers import *
from lib.classes import Conversation

from munch import Munch
from munch import munchify

from app import thread_lock
from app import thread_unlock
from app import get_common_vars
from app import llm
from app import flask_app

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

@flask_app.post("/v1")
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


@flask_app.get("/v1/session/<session_name>")
async def v1_session_n_GET(session_name):
    try:
        await thread_lock()
        global llm

        convo = Conversation(session_name, llm)
        convo.load()
        thread_unlock()

        convo.session.messages = convo.get_messages()
        return convo.session
    except:
        thread_unlock()
        return ""

@flask_app.post("/v1/session/<session_name>")
async def v1_session_n_POST(session_name):
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
                convo.add_message(convo.session.user_name, o["context"])

        query = o["query"]
        query_message = convo.add_message(convo.session.user_name, query)
        reply = convo.get_response(query)
        reply_message = convo.add_message(convo.session.assistant_name, reply)

        convo.save()
        thread_unlock()

        return {
            "query": query_message,
            "reply": reply_message
        }
    except Exception as x:
        print(x)
        pass

    thread_unlock()
    return { "reply": "Error" }

@flask_app.post("/v1/session/<session_name>/rename")
async def v1_session_n_rename_POST(session_name):
    try:
        await thread_lock()
        global llm

        o = request.json
        new_session_name = o["new_session_name"]
        convo = Conversation(session_name, llm)
        convo.load()
        convo.save(new_session_name)
        convo.delete()

        thread_unlock()
        return { "session_name": new_session_name }
    except Exception as x:
        print(x)
        pass

    thread_unlock()
    return { "session_name": session_name }

@flask_app.post("/v1/session/<session_name>/saveas")
async def v1_session_n_saveas_POST(session_name):
    try:
        await thread_lock()
        global llm

        o = request.json
        new_session_name = o["new_session_name"]
        convo = Conversation(session_name, llm)
        convo.load()
        convo.save(new_session_name)

        thread_unlock()
        return { "session_name": new_session_name }
    except Exception as x:
        print(x)
        pass

    thread_unlock()
    return { "session_name": session_name }

@flask_app.post("/v1/session/<session_name>/delete")
async def v1_session_n_delete_POST(session_name):
    try:
        await thread_lock()
        global llm

        o = request.json
        convo = Conversation(session_name, llm)
        convo.delete()

        thread_unlock()
        return { "deleted": True }
    except:
        pass

    thread_unlock()
    return { "deleted": False }

@flask_app.post("/v1/session/<session_name>/reset")
async def v1_session_n_reset_POST(session_name):
    try:
        await thread_lock()
        global llm

        o = request.json

        last_n_messages = None
        if "last_n_messages" in o:
            last_n_messages = o["last_n_messages"]

        convo = Conversation(session_name, llm)

        if last_n_messages is None:
            if "last_n_messages" in convo.session:
                last_n_messages = convo.session.last_n_messages

        if isinstance(last_n_messages, int):
            convo.load(last_n_messages)

        convo.save()

        thread_unlock()
        return { "reset": True }
    except:
        pass

    thread_unlock()
    return { "reset": False }

@flask_app.post("/v1/session/<session_name>/settings")
async def v1_session_n_settings_POST(session_name):
    try:
        await thread_lock()

        o = request.json
        convo = Conversation(session_name)

        for key in ["name", "user_name", "assistant_name", "context", "last_n_messages", "locked", "display_as_contact"]:
            if key in o:
                convo.session_set(key, o[key])

        convo.save()

        if convo.session.name != session_name:
            if convo.session.locked == False or convo.session.locked is None:
                old_convo = Conversation(session_name)
                old_convo.delete()

        thread_unlock()
        return { "session_name": convo.session.name }
    except:
        pass

    thread_unlock()
    return { "session_name": session_name }

@flask_app.post("/v1/session/<session_name>/message/<message_id>/save")
async def v1_session_n_message_n_save_POST(session_name, message_id):
    try:
        await thread_lock()
        global llm

        o = request.json

        convo = Conversation(session_name, llm)

        for i in range(0, len(convo.session.messages)):
            m = convo.session.messages[i]

            if int(m["id"]) != int(message_id):
                continue
        
            for key in ["body", "hidden"]:
                if key in o:
                    m[key] = o[key]

            convo.session.messages[i] = m

        convo.save()

        thread_unlock()
        return { "saved": True }
    except:
        pass

    thread_unlock()
    return { "saved": False }

@flask_app.post("/v1/session/<session_name>/message/<message_id>/delete")
async def v1_session_n_message_n_delete_POST(session_name, message_id):
    try:
        await thread_lock()
        global llm

        o = request.json

        convo = Conversation(session_name, llm)

        new_messages = []

        for i in range(0, len(convo.session.messages)):
            m = convo.session.messages[i]

            if int(m["id"]) == int(message_id):
                continue

            new_messages.append(m)

        convo.session.messages = new_messages
        convo.save()

        thread_unlock()
        return { "deleted": True }
    except:
        pass

    thread_unlock()
    return { "deleted": False }
