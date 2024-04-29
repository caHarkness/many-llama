# Session

A **session** is a conversation session stored as a JSON file in the `sessions/` directory relative to the project and is represented as a thread of back-and-forth messages between a user (yourself) and an assistant.

You can interact with a session by providing text input at the bottom of the view and either clicking the blue send button or by pressing enter. Your message will be added to the history of previous messages and a reply will automatically be generated based on the starting context and the included message history. The reply will then also be added to the message history.

---

## Features

* **Search** — Use the input at the top of the view to filter messages for bodies containing the text supplied. If the search term contains more than one word separated by spaces, the terms are searched for individually. For the message to show, the message body must contain the words provided, but not necessarily as an exact match.

* **Favorites** — Shows a list of favorite messages that can be searched and sent immediately 

* **Edit** — Click to enable per-message editing. To edit a message, click its edit icon next to the author's name and edit the text as needed. To sumbit the text changes, click the green save icon. From this view, you may also toggle the favorite and hidden status of the message, or delete the message entirely.

* **Reset** — Only shown when `last_n_messages` has a value. Select this option to reset to a number of preserved messages from the bottom or the top of the message history. 

* **Settings** — Configure this session using the web interface.

---

## JSON

A session is the following in JSON:

    {
        "name": "default",
        "user_name": "User",
        "assistant_name": "Assistant",
        "context": "This is a conversation...",
        "last_n_messages": -1,
        "display_as_contact": false,
        "messages": [
            {
                "id": 0,
                "author": "user",
                "body": "What is the distance...",
                "time": "2024-04-17 12:12:57.000",
                "hidden": true,
                "favorite": false
            },
            {
                "id": 1,
                "author": "assistant",
                "body": "The distance is...",
                "time": "2024-04-17 12:13:00.000",
                "hidden": true,
                "favorite": false
            }
        ]
    }

Here are the fields broken down:

* `name` — The name of the session. This field is never read from but is written to every time the session is modified and should match the name of the JSON file without the extension.

* `user_name` — The display name of the user (you). Modify this to change who messages from yourself appear to be from.

* `assistant_name` — The display name of the assistant. Modify this to change who messages from the assistant appear to be from.

* `context` — A description of what the LLM is looking at to help it predict what comes next.

* `last_n_messages` — A `null` or integer value that enables the reset feature. If the value is positive, resetting keeps that number of messages from the end of the message history. If the value is negative, resetting takes the absolute value of that number and keeps that many messages from the start of the message history. If the value is `null`, the reset feature is disabled and all messages are always included in the text submitted to the LLM.

    **Tip:** To help the LLM into giving better responses, sometimes a starter conversation is needed. The reset feature in combination with a negative value for `last_n_messages` is a powerful way to get more precise and desirable results.

* `display_as_contact` — A boolean value controlling whether the name of the session or the assistant's name is shown as the thread's title. Setting this to true gives this thread the appearance of having a conversation with a saved contact.

* `messages` — An array of message objects that build the message history.

        {
            "id": 0,
            "author": "user",
            "body": "What is the distance...",
            "time": "2024-04-17 12:12:57.000",
            "hidden": true,
            "favorite": false
        },

    * `id` — A unique ID for the message specific to the conversation session it belongs to.

    * `author` — A string field containing either `user` or `assistant` that controls how this message is displayed to the user and how it is formatted for the LLM.

    * `body` — A string field containing the contents of the message.

    * `time` — The date and time this message was submitted or generated at.

    * `hidden` — A boolean controlling whether this message starts hidden from the thread view.

    * `favorite` — A boolean controlling whether this message's body is shown in the list of meavorite messages.
