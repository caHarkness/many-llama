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

st.session_state.settings = Helpers.read_json("settings.json", {
    "default_context": DEFAULT_CONTEXT
})

# Called 
def make_chat_function(chat_name):
    def _callable():
        convo = Chat(chat_name)

        @st.dialog("Rename")
        def rename():
            new_name = st.text_input("Name", value=chat_name)
            if st.button("Save"):
                convo.save(new_chat_name=new_name)
                convo.delete()
                make_chat_pages()
                st.switch_page(globals()[f"chat_{new_name}_page"])

        @st.dialog("Save as")
        def save_as():
            new_name = st.text_input("Name", value=chat_name)
            if st.button("Save"):
                convo.save(new_chat_name=new_name)
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

            st.session_state.run = 1
            st.rerun()

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
            if len(convo.get_messages()) > 0: st.button("Undo", on_click=undo, use_container_width=True)
            if len(convo.get_messages()) > 0: st.button("Redo", on_click=redo, use_container_width=True)

            st.button("Rename", on_click=rename, use_container_width=True)
            st.button("Save as", on_click=save_as, use_container_width=True)
            st.button("Delete", on_click=delete, use_container_width=True)

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

def home():
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
    default_context = st.text_area("Default Context", value=st.session_state.settings["default_context"])

    if st.button("Save"):
        st.session_state.settings["default_context"] = default_context

        Helpers.write_file(
            "settings.json",
            json.dumps(st.session_state.settings, indent=4))

        st.toast("Settings saved.")

def about():
    markdown_text = Helpers.read_file("README.md")
    st.markdown(markdown_text)
        

globals()["home_page"]      = st.Page(home, title="New", icon=":material/post_add:")
globals()["settings_page"]  = st.Page(settings, title="Settings", icon=":material/settings:")
globals()["about_page"]     = st.Page(about, title="About", icon=":material/info:")

chats_term = "Chats"
if "search_query" in st.session_state:
    if len(st.session_state.search_query) > 0:
        chats_term = "Results"

pg = st.navigation({
    "File":     [home_page, settings_page, about_page],
    chats_term: make_chat_pages()
})

search_query = st.sidebar.text_input("Search")
if st.sidebar.button("Go"):
    st.session_state.search_query = search_query
    st.rerun()

st.sidebar.caption("Many Llama v1.0.100")

if st.sidebar.button("Reload", use_container_width=True):
    st.write("Refresh this page manually.")
    # Streamlit devs, why do you make it hard to exit your application?
    os._exit(0)
    st.stop()

pg.run()
