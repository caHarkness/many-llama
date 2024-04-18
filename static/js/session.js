$(function() {
    fnGetSessionName = function()
    {
        return $("[name='session-name']").first().val();
    };

    fnClear = function()
    {
        $.ajax({
            url: `/session/${fnGetSessionName()}/clear`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                dummy: "data"
            }),
            success: function(data)
            {
                fnRefresh();
            }
        });
    };

    fnClearSearch = function()
    {
        $("[name='search-text']")
            .first()
            .val("")
            .trigger("input");
    };

    fnShowRenameModal = function()
    {
        $("#rename-modal").modal("show");
        $("[name='new-name']").first().focus();
    };

    fnRename = function()
    {
        newName = $("[name='new-name']").first().val();

        FormValidator.onPass(function() {
            $.ajax({
                url: `/v1/session/${fnGetSessionName()}/rename`,
                type: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                data: JSON.stringify({
                    new_session_name: newName
                }),
                success: function(data)
                {
                    window.location.href = `/session/${data.session_name}`;
                }
            });
        });
    };

    fnShowSaveAsModal = function()
    {
        $("#save-as-modal").modal("show");
        $("[name='new-name']").first().focus();
    };

    fnSaveAs = function()
    {
        newName = $("[name='new-name']").first().val();

        FormValidator.onPass(function() {
            $.ajax({
                url: `/v1/session/${fnGetSessionName()}/saveas`,
                type: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                data: JSON.stringify({
                    new_session_name: newName
                }),
                success: function(data)
                {
                    window.location.href = `/session/${data.session_name}`;
                }
            });
        });
    };

    fnShowSettingsModal = function()
    {
        $("#conversation-settings-modal [name='user_name']").val(GlobalSessionData.user_name);
        $("#conversation-settings-modal [name='assistant_name']").val(GlobalSessionData.assistant_name);
        $("#conversation-settings-modal [name='context']").val(GlobalSessionData.context);
        $("#conversation-settings-modal [name='last_n_messages']").val(GlobalSessionData.last_n_messages);
        $("#conversation-settings-modal [name='locked']").prop("checked", GlobalSessionData.locked);

        $("#conversation-settings-modal").modal("show");
    };

    fnSaveSettings = function()
    {

        var last_n_messages = $("#conversation-settings-modal [name='last_n_messages']").first().val();

        $.ajax({
            url: `/v1/session/${fnGetSessionName()}/settings`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                user_name:          $("#conversation-settings-modal [name='user_name']").first().val(),
                assistant_name:     $("#conversation-settings-modal [name='assistant_name']").first().val(),
                context:            $("#conversation-settings-modal [name='context']").first().val(),
                last_n_messages:
                    last_n_messages.length > 0?
                        parseInt(last_n_messages) :
                        null,
                locked:             $("#conversation-settings-modal [name='locked']").first().is(":checked")
            }),
            success: function(data)
            {
                window.location.href = window.location.href;
            }
        });
    };

    fnDelete = function()
    {
        $.ajax({
            url: `/v1/session/${fnGetSessionName()}/delete`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                session_name: fnGetSessionName()
            }),
            success: function(data)
            {
                window.location.href = `/`;
            }
        });
    };

    GlobalSessionData = {};

    fnRefresh = function()
    {
        $.ajax({
            url: `/v1/session/${fnGetSessionName()}`,
            type: "GET",
            success: function(session)
            {
                GlobalSessionData = session;

                $("#messages").html("");

                for (o in session.messages)
                {
                    o = session.messages[o];
                    fnAddMessage(o);
                }

                window.scrollTo(0, document.body.scrollHeight);
                $("[name='user-input']").first().focus();
            }
        });
    };

    fnReset = function()
    {
        $.ajax({
            url: `/v1/session/${fnGetSessionName()}/reset`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                last_n_messages: null
            }),
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

    fnAddMessage = function(m)
    {
        if (typeof(m) === "undefined")
            return;

        var div = $($(".message-template").first().html());

        if (m.hidden)
            div.addClass("hidden-message d-none opacity-50");

        div.find(".message-id").first().html(m.id);
        div.find(".message-author").first().html(m.author_name);
        div.find(".message-body").first().html(m.body);
        div.find(".message-body-original").first().html(m.body);

        switch (m.type)
        {
            case "query":
                div.addClass("query");
                div.find(".message-body").first().addClass("alert alert-primary mb-1");
                break;

            case "reply":
                div.addClass("reply");
                div.find(".message-body").first().addClass("alert alert-secondary mb-1");
                break;
        }

        $("#messages").first().append(div);
        return div;
    };

    fnSend = async function()
    {
        var input = $("[name='user-input']").first();
        var text = input.val();

        input.val("");

        var tempQuery = fnAddMessage({ id: -1, author_name: GlobalSessionData.user_name, body: text, type: "query" });
        var tempReply = fnAddMessage({ id: -1, author_name: GlobalSessionData.assistant_name, body: "...", type: "reply" });

        window.scrollTo(0, document.body.scrollHeight);

        var ajaxResponse = null;

        $.ajax({
            url: `/v1/session/${fnGetSessionName()}`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                query: text
            }),
            success: function(data) { ajaxResponse = data; },
            error: function(xhr, x) { ajaxResponse = {}; }
        });

        while (ajaxResponse == null)
            await new Promise(r => setTimeout(r, 100));

        tempQuery.remove();
        tempReply.remove();

        fnAddMessage(ajaxResponse.query);
        fnAddMessage(ajaxResponse.reply);

        window.scrollTo(0, document.body.scrollHeight);
    };

    fnShowHidden = function()
    {
        $(".hidden-message").removeClass("d-none");
    };

    fnEditPage = function()
    {
        fnShowHidden();
        $(".message-control-link").removeClass("d-none");
    };

    fnEditMessage = function(e)
    {
        e = $(e);

        var parent = e.parents(".message-wrapper").first();
        var controlContainer = parent.find(".message-control-container").first();

        fnCancelEditMessage();

        var body = parent.find(".message-body").first();
        var bodyWidth = body.width();
        var bodyText = body.text();

        body.html("");
        var editable = $("<textarea></textarea>");
        editable.addClass("w-100");
        editable.val(bodyText);
        editable.attr("rows", 3);
        body.addClass("w-75");
        body.append(editable);

        $(".message-control-container").each(function(i, x) {
            x = $(x);
            x.html("");
        });

        var controls = $(".message-controls").first().clone();

        controlContainer.append(controls);
    };

    fnCancelEditMessage = function()
    {
        $("#messages div.message-wrapper").each(function(i, x) {
            x = $(x);
            var body = x.find(".message-body").first();
            body.removeClass("w-75");

            var textarea = body.find("textarea");
            if (textarea.length > 0)
            {
                textarea = textarea.first();
                var textareaText = textarea.val();
                //body.html(textareaText);
                body.html(x.find(".message-body-original").html());
            }

            x.find(".message-control-container")
                .first()
                .html("");
        });
    };

    fnSaveMessage = function(e)
    {
        e = $(e);
        var parent = e.parents(".message-wrapper").first();
        var id = parent.find(".message-id")
            .first()
            .html()
            .trim();

        var textarea = parent.find(".message-body textarea");

        if (textarea.length < 1)
            return;

        textarea = textarea.first();
        textareaText = textarea.val();

        $.ajax({
            url: `/v1/session/${fnGetSessionName()}/message/${id}/save`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                body: textareaText
            }),
            success: function(data)
            {
                if (data.saved)
                {
                    parent.find(".message-body-original").html(textareaText);
                    fnCancelEditMessage();
                }
            }
        });
    };

    fnHideMessage = function(e, hidden)
    {
        e = $(e);
        var parent = e.parents(".message-wrapper").first();
        var id = parent.find(".message-id")
            .first()
            .html()
            .trim();

        $.ajax({
            url: `/v1/session/${fnGetSessionName()}/message/${id}/save`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                hidden: hidden
            }),
            success: function(data)
            {
                if (data.saved)
                {
                    parent.removeClass("hidden-message opacity-50");
                    parent.find("hide-message-btn").first().addClass("d-none");
                    parent.find("unhide-message-btn").first().addClass("d-none");

                    if (hidden)
                    {
                        parent.addClass("hidden-message opacity-50");
                        parent.find("unhide-message-btn").first().removeClass("d-none");
                    }

                    else
                    {
                        parent.find("hide-message-btn").first().removeClass("d-none");
                    }

                }
            }
        });
    };

    fnDeleteMessage = function(e)
    {
        e = $(e);
        var parent = e.parents(".message-wrapper").first();
        var id = parent.find(".message-id")
            .first()
            .html()
            .trim();

        $.ajax({
            url: `/v1/session/${fnGetSessionName()}/message/${id}/delete`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                session_name: fnGetSessionName()
            }),
            success: function(data)
            {
                if (data.deleted)
                    parent.remove();
            }
        });
    };

    fnBind = function()
    {
        $(document).unbind("keyup");
        $(document).on("keyup", function(e) {
            if (e.keyCode == 13)
                if ($("[name='user-input']").is(":focus"))
                    fnSend();
        });

        $("[name='search-text']").unbind("input");
        $("[name='search-text']").on("input", function() {
            elem = $(this);
            text1 = elem.val();

            $("#messages div.message-wrapper").each(function(i, x) {
                x = $(x);
                text2 = x.text();

                x.hide();
                //if (text2.match(new RegExp(text1)))
                if (text2.hasWords(text1))
                    x.show();
            });
        });
    };

    fnBind();
    fnRefresh();
});
