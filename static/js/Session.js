$(function() {
    Session = {};
    Session.data = {};

    Session.fnGetName = function()
    {
        return $("[name='session-name']").first().val();
    };

    Session.fnRefresh = function()
    {
        $.ajax({
            url: `/v1/session/${Session.fnGetName()}`,
            type: "GET",
            success: function(session)
            {
                Session.data = session;

                $("#messages").html("");

                for (o in session.messages)
                    SessionPage.fnAddMessage(session.messages[o]);

                window.scrollTo(0, document.body.scrollHeight);
                $("[name='user-input']").first().focus();
            }
        });
    };

    Session.fnReset = function()
    {
        $.ajax({
            url: `/v1/session/${Session.fnGetName()}/reset`,
            type: "POST",
            headers: Common.fnGetAPIHeaders(),
            data: JSON.stringify({}),
            success: function(data)
            {
                // Reload the page:
                window.location.href =
                    window.location.href;
            }
        });
    };

    fnMakeReplyReplacements = function(str)
    {
        if (str.match(/```/g))
        {
            str = str.replace(/```.*\n([\s\S]{1,})```/g, "<pre>$1</pre>");
        }
        else
        {
            if (str.match(/\n/g))
                str = str.replace(/\n/g, "<br />");
        }

        return str;
    };

    Session.fnSend = async function()
    {
        var input = $("[name='user-input']").first();
        var text = input.val();

        if (text.trim().length < 1)
            return;

        input.val("");

        var tempQuery = SessionPage.fnAddMessage({ id: -1, author_name: Session.data.user_name, body: text, type: "query" });
        var tempReply = SessionPage.fnAddMessage({ id: -1, author_name: Session.data.assistant_name, body: "...", type: "reply" });

        window.scrollTo(0, document.body.scrollHeight);

        var ajaxResponse = null;

        $.ajax({
            url: `/v1/session/${Session.fnGetName()}`,
            type: "POST",
            headers: Common.fnGetAPIHeaders(),
            data: JSON.stringify({
                query: text
            }),
            success: function(data) { ajaxResponse = data; },
            error: function(xhr, x) { ajaxResponse = {}; }
        });

        while (ajaxResponse == null)
            await new Promise(r => setTimeout(r, 100));

        //tempQuery.remove();
        //tempReply.remove();
        tempQuery.replaceWith(SessionPage.fnAddMessage(ajaxResponse.query, false));
        tempReply.replaceWith(SessionPage.fnAddMessage(ajaxResponse.reply, false));

        window.scrollTo(0, document.body.scrollHeight);
    };

    Session.fnRefresh();
});
