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

'''
Get the conversation in JSON form via a GET request:
'''
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

'''
Add to the conversation and get a reply via a POST request:
'''
@flask_app.post("/v1/session/<session_name>")
async def v1_session_n_POST(session_name):
    try:
        await thread_lock()
        global llm
        o               = request.json
        convo           = Conversation(session_name, llm)
        last_n_messages = None

        # If the settings key is found, change settings and exit early:
        if "settings" in o:
            if isinstance(o["settings"], dict):
                settings = o["settings"]

                for key in ["name", "user_name", "assistant_name", "context", "last_n_messages", "display_as_contact"]:
                    if key in settings:
                        convo.session_set(key, settings[key])

                convo.save()

                # If the name was changed in the settings, delete the old conversation:
                if convo.session.name != session_name:
                    old_convo = Conversation(session_name)
                    old_convo.delete()
                
                thread_unlock()
                return { "session_name": convo.session.name }

        # If the delete key is found and is true, delete and exit early:
        if "delete" in o:
            if o["delete"] == True:
                convo.delete()
                thread_unlock()
                return { "success": True }

        # If the reset key is found and is true, reset and exit early:
        if "reset" in o:
            if o["reset"] == True:
                if "last_n_messages" in o:
                    last_n_messages = o["last_n_messages"]

                if last_n_messages is None:
                    if "last_n_messages" in convo.session:
                        last_n_messages = convo.session.last_n_messages

                if isinstance(last_n_messages, int):
                    convo.load(last_n_messages)

                convo.save()
                thread_unlock()
                return { "success": True }


        if "last_n_messages" in o:
            last_n_messages = int(o["last_n_messages"])

        if "clear_session" in o:
            if o["clear_session"] == 1:
                last_n_messages = 0

        convo.load(last_n_messages)

        if last_n_messages == 0:
            if "context" in o:
                convo.add_message(convo.session.user_name, o["context"])

        query           = None
        query_message   = None
        if "query" in o:
            if o["query"] is not None and len(o["query"]) > 0:
                query = o["query"]
                query_message = convo.add_message(convo.session.user_name, query)

        reply           = None
        reply_message   = None
        if "get_reply" in o:
            if o["get_reply"] == True:
                reply = convo.get_reply()
                reply_message = convo.add_message(convo.session.assistant_name, reply)

        convo.save()
        thread_unlock()

        return {
            "success": True,
            "query": query_message,
            "reply": reply_message
        }
    except Exception as x:
        print(x)
        thread_unlock()
        return {
            "success": False,
            "message": str(x)
        }
        pass

'''
Manipulate session messages via a session name and the message id via a POST request:
'''
@flask_app.post("/v1/session/<session_name>/message/<message_id>")
async def v1_session_n_message_n_POST(session_name, message_id):
    try:
        await thread_lock()
        o               = request.json
        convo           = Conversation(session_name)
        new_messages    = []

        for i in range(0, len(convo.session.messages)):
            m = convo.session.messages[i]
        
            if int(m["id"]) == int(message_id):
                for key in ["body", "favorite", "hidden", "delete"]:
                    if key in o:
                        m[key] = o[key]

            if "delete" in m:
                if m["delete"] == True:
                    continue

            new_messages.append(m)

        convo.session.messages = new_messages
        convo.save()
        thread_unlock()
        return { "success": True }

    except Exception as x:
        print(x)
        thread_unlock()
        return {
            "success": False,
            "message": str(x)
        }
        pass

@flask_app.get("/v1/favorites")
async def v1_favorites():
    try:
        common = get_common_vars()
        return common.favorites
    except Exception as x:
        pass
