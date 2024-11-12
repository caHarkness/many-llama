import sys

sys.path.append(".")

import os
import signal
import re
import json

import streamlit as st

from manyllama import Helpers
from manyllama import Chat

for x in os.environ:
    globals()[x] = os.environ[x]

class Settings():
    def load():
        st.session_state.settings = Helpers.read_json("settings.json", {
            "default_context": DEFAULT_CONTEXT,
            "developer_mode": False
        })

    def save():
        Helpers.write_file(
            "settings.json",
            json.dumps(st.session_state.settings, indent=4))

        Settings.load()

    def get(key, default_value=None, save=False):
        if "settings" not in st.session_state:
            Settings.load()

        if key in st.session_state.settings:
            return st.session_state.settings[key]
        else:
            if save:
                Settings.set(key, default_value)
            return default_value

    def set(key, value):
        if "settings" not in st.session_state:
            Settings.load()
        st.session_state.settings[key] = value
        Settings.save()

    def render(name, key, kind, options={}):
        setting_key = f"setting_{key}"

        def on_change():
            val = st.session_state[setting_key]
            print(f"Set {key} to {val}")
            Settings.set(key, val)

        kind(
            name,
            value=Settings.get(key),
            key=setting_key,
            on_change=on_change,
            **options)
            


Settings.load()

# Called 
def make_chat_function(chat_name):
    def _callable():
        convo = Chat(chat_name)

        @st.dialog("Edit Chat")
        def edit_chat():

            new_name    = st.text_input("Name", value=chat_name)
            new_context = st.text_area("Context", value=convo.data["context"])
            save_as     = st.toggle("Save as a copy", value=False)

            if st.button("Save"):
                convo.data["context"] = new_context
                convo.save(new_chat_name=new_name)

                if save_as == False:
                    convo.delete()

                make_chat_pages()
                st.switch_page(globals()[f"chat_{new_name}_page"])

        @st.dialog("Delete")
        def delete():
            st.write("Are you sure you want to delete this conversation?")

            if st.button("Delete"):
                convo.delete()
                st.switch_page(home_page)

        # Begin rendering the page's content:
        st.title(chat_name)
        st.caption("This is the beginning of the conversation")

        for m in convo.get_messages():
            with st.chat_message(m["author"]):
                st.markdown(m["body"])

        if "run" in st.session_state:
            if st.session_state.run == 1:
                with st.chat_message("assistant"):
                    reply = st.write_stream(convo.stream_reply())
                    convo.add_message(convo.data["assistant_name"], reply)
                    convo.save()
                st.session_state.run = 0

        # Accept user input
        if query := st.chat_input("Say something"):
            convo.add_message(convo.data["user_name"], query)
            convo.save()

            if Settings.get("autorun", True):
                st.session_state.run = 1

            st.rerun()

        def run():
            st.session_state.run = 1

        def undo():
            while True:
                m = convo.get_last_message()
                if m["author"] == convo.data["assistant_name"]:
                    convo.data["messages"] = convo.data["messages"][:-1]
                else:
                    break

            if len(convo.get_messages()) > 0:
                convo.data["messages"] = convo.data["messages"][:-1]

            convo.save()

        def redo():
            if len(convo.get_messages()) > 0:
                convo.data["messages"] = convo.data["messages"][:-1]
                convo.save()

                st.session_state.run = 1
                #st.rerun()

        with st.popover("...") as pop:
            if Settings.get("autorun", True) == False:
                st.button("Run", on_click=run, use_container_width=True, icon=":material/play_arrow:")

            if len(convo.get_messages()) > 0:
                st.button("Undo", on_click=undo, use_container_width=True, icon=":material/undo:")
                st.button("Redo", on_click=redo, use_container_width=True, icon=":material/replay:")

            st.button("Edit", on_click=edit_chat, use_container_width=True, icon=":material/description:")
            st.button("Delete", on_click=delete, use_container_width=True, icon=":material/delete:")
            

    _callable.__name__ = f"chat_{chat_name}"
    return _callable


def get_sorted_chats():
    chats = []
    for o in os.listdir("chats"):
        if os.path.isfile(f"chats/{o}"):
            if re.search(r"\.json$", o):
                chat_name = re.sub(r"\.json$", "", o)
                c = Chat(chat_name)
                chats.append(c)

    def sort_by_time(chat):
        m = chat.get_last_message()
        if m is not None:
            return m["time"]
        return 0

    chats = sorted(chats, key=lambda chat: sort_by_time(chat), reverse=True)
    return chats

def make_chat_pages():
    pages = []

    for chat in get_sorted_chats():
        chat_name                       = chat.data["name"]
        chat_function_name              = f"chat_{chat_name}"
        chat_page_name                  = f"{chat_function_name}_page"
        globals()[chat_function_name]   = make_chat_function(chat_name)

        chat_page                       = st.Page(globals()[chat_function_name], title=f"{chat_name}", icon=":material/forum:")
        globals()[chat_page_name]       = chat_page

        if "search_query" in st.session_state:
            if len(st.session_state.search_query) > 0:
                search_query        = st.session_state.search_query.lower()
                search_query_parts  = search_query.split(" ")
                found               = 1

                for part in search_query_parts:
                    if len(part) < 1:
                        continue

                    if part not in chat.get_serialized().lower():
                        found = 0

                if found == 0:
                    continue

        pages.append(chat_page)

    return pages



def new():
    if Settings.get("quick_create", True):
        st.title("New")
        st.caption("This is the beginning of the conversation")

        # Accept user input
        if query := st.chat_input("Say something"):
            c = Chat()
            chat_name = c.data["name"]
            c.data["context"] = Settings.get("default_context")
            c.add_message(c.data["user_name"], query)
            c.save()
            make_chat_pages()
            st.session_state.run = 1
            st.switch_page(globals()[f"chat_{chat_name}_page"])

        return

    chat_name   = st.text_input("Name", value="default")
    new_context = st.text_area("Context", value=st.session_state.settings["default_context"])

    if st.button("Create"):
        c = Chat(chat_name)
        c.data["context"] = new_context
        c.save()

        if "search_query" in st.session_state:
            del st.session_state.search_query

        make_chat_pages()
        st.switch_page(globals()[f"chat_{chat_name}_page"])

def settings():
    Settings.render("Default Context", "default_context", st.text_area)
    Settings.render("Quick Create", "quick_create", st.toggle)
    Settings.render("Show Search", "show_search", st.toggle)
    Settings.render("Developer Mode", "developer_mode", st.toggle)

def ask():
    # Accept user input
    if q := st.chat_input("Say something"):
        question = q

        if not re.search(r"\?", question):
            st.toast("Please include a question mark.")
            return

        matches         = re.search(r"^(.*\?+)(.*)$", question)
        question        = matches.group(1)
        instructions    = matches.group(2)

        with st.chat_message("user"):
            st.write(question)

        chats = get_sorted_chats()
        total_text = ""

        with st.spinner("Fetching"):
            for chat in chats:
                contains_answer, answer = chat.contains_answer_to(question, return_answer=True)
                chat_name = chat.data["name"]

                if contains_answer:
                    total_text = f"{total_text}\n\nFrom chat named \"{chat_name}\": {answer}"

        c = Chat("summarizer")

        c.add_message(c.data["user_name"], f"Summarize the following: \n\n {total_text}\n\n{instructions}")

        with st.chat_message("assistant"):
            reply = st.write_stream(c.stream_reply())

def about():
    markdown_text = Helpers.read_file("README.md")
    st.markdown(markdown_text)

globals()["new_page"]       = st.Page(new, title="New", icon=":material/post_add:")
globals()["settings_page"]  = st.Page(settings, title="Settings", icon=":material/settings:")
globals()["ask_page"]       = st.Page(ask, title="Ask", icon=":material/campaign:")
globals()["about_page"]     = st.Page(about, title="About", icon=":material/info:")

chats_term = "Chats"
if "search_query" in st.session_state:
    if len(st.session_state.search_query) > 0:
        chats_term = "Results"

pg = st.navigation({
    "File":     [new_page, settings_page, ask_page, about_page],
    chats_term: make_chat_pages()
})

if Settings.get("show_search", True, True):
    search_query = st.sidebar.text_input("Search")
    if st.sidebar.button("Go"):
        st.session_state.search_query = search_query
        st.rerun()

st.sidebar.caption("Many Llama v1.0.101")

if Settings.get("developer_mode"):
    Settings.render("Autorun", "autorun", st.sidebar.toggle)


    if st.sidebar.button("Restart", use_container_width=True, icon=":material/power_settings_new:"):
        st.write("Refresh this page manually.")
        # Streamlit devs, why do you make it hard to exit your application?
        os._exit(0)
        st.stop()

pg.run()
