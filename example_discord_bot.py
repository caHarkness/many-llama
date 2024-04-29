'''
How to use:

1. Get many-llama with web interface running.
2. ". ./venv/bin/activate && pip install discord"
3. Host the many-llama Flask API and modify API_LOCATION in this Python script to access it.
4. Create a Discord bot with permissions to read and send messages to a channel.
5. Invite the bot to a server and set the channel topic to something like:

    You will obey my orders as an assistant. You will roleplay as a person named Bob. You, as Bob, will only reply with giddy and happy-go-lucky responses. Bob is not insulting and Bob will always show extreme enthusiasm. Starting now, you are Bob.

6. In the channel: tag the bot, write a message to it, and send the message.
7. Wait for a response.

If the many-llama API is running with GPU acceleration, the reply should come in seconds. What happened during this time? The bot responds to all messages it is tagged in. If the last activity from the user in a channel is greater than 5 minutes, clear the session. When a new session is created, the channel's topic is sent as the first message to the LLM, immediately followed by the Discord user's message. For example, when you say "@Bot Hello!" the following happens:

---

User: You will obey my orders as an assistant. You will roleplay as a person named Bob. You, as Bob, will only reply with giddy and happy-go-lucky responses. Bob is not insulting and Bob will always show extreme enthusiasm. Starting now, you are Bob.

User: Hello!

Assitant: Hi user! My name is Bob! I am excited to help you!

---

The first message from "User" is not seen in or posted to Discord. It is silently sent to the LLM as a method to build context using the Discord channel's topic. This allows for the server owner to create multiple rooms with various functions. For example, if the channel topic instructs the assistant to "translate all my messages to Korean," the channel immediately becomes a translation tool.

The user tagging the bot has 5 minutes to reply to the conversation after their last message. In order to continue talking to the bot, the user must tag the bot in every message they send. If the user replies within 5 minutes, the message history is not cleared and the conversation can continue. After a 5 minute break, the session is cleared and starts anew. To disable this behavior, change the line below from "CLEAR_SESSION_DEFAULT = 1" to "CLEAR_SESSION_DEFAULT = 0".

Note: Session names are channel name and username specific. For example, Discord user "Joe" writing messages to the bot in a channel named "some-channel-name" will open a many-llama session named "some-channel-name_Joe" and isolate Joe's messages from other channels and other users. Other users cannot influence or interact with Joe's session. Information written to the bot in one channel will not bleed into another. For example: if Joe tells the bot in one channel "Please call me master," the bot in other channels will not call Joe "master" unless also instructed to do so in those channels.
'''

# Configuration:
API_LOCATION            = "http://127.0.0.1:8010"
CLEAR_SESSION_DEFAULT   = 1

# Imports:
import discord
import re
import requests
import time

from lib.helpers import *

intents         = discord.Intents(messages=True, guilds=True, message_content=True, reactions=True)
client          = discord.Client(intents=intents)
session_times   = {}

# When the Discord bot starts up successfully:
@client.event
async def on_ready():
    print("READY")

# Non-blocking POST request function for accessing the Flask API:
async def get_response(session_name, input_dict):
    return requests.post(
        f"{API_LOCATION}/v1/session/{session_name}",
        json=input_dict)

# When the Discord bot sees a new message anywhere:
@client.event
async def on_message(msg):
    chl = msg.channel

    # If the bot is tagged in the message it receives for this event:
    if client.user.id in msg.raw_mentions:
        user_name       = msg.author.name
        session_name    = f"{chl.name}_{user_name}"

        # Clear the session if the user has been inactive for 5 minutes:
        clear_session = CLEAR_SESSION_DEFAULT
        if session_name in session_times.keys():
            time_diff = time.perf_counter() - session_times[session_name]
            if time_diff < 60 * 5:
                clear_session = 0

        # Get rid of the text used to tag the bot:
        exclusion           = f"<@{client.user.id}>"
        scrubbed_message    = re.sub(exclusion, "", msg.content)
        scrubbed_message    = scrubbed_message.strip()

        # Use the channel's topic as context for the conversation with the LLM:
        context = chl.topic
        if context is None or len(context.strip()) < 1:
            context = ""

        # If the message is a reply to another, include that message as context:
        user_message = scrubbed_message
        if msg.reference is not None:
            ref             = await chl.get_partial_message(msg.reference.message_id).fetch()
            user_message    = f"{ref.content}\n\n{user_message}"

        await chl.typing()

        resp = await get_response(session_name, {
            "context":          context,
            "query":            user_message,
            "clear_session":    clear_session,
            "get_reply":        True
        })

        resp = json.loads(resp.text)
        resp = resp["reply"]["body"]

        await chl.send(resp)

        session_times[session_name] = time.perf_counter()

# Start the Discord bot using the contents of the token.txt file:
client.run(read_file("token.txt", ""))
