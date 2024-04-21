$(function() {
    SessionMessage = {};

    SessionMessage.fnEdit = function(e)
    {
        e = $(e);

        var parent = e.parents(".message-wrapper").first();
        var controlContainer = parent.find(".message-control-container").first();

        SessionMessage.fnCancelEdit();

        var body = parent.find(".message-body").first();
        var bodyWidth = body.width();
        var bodyHeight = body.height();
        var bodyText = body.text();

        body.html("");

        var textarea = $("<textarea></textarea>");
        textarea.addClass("w-100");
        textarea.val(bodyText);
        textarea.attr("rows", 3);
        

        body.addClass("w-75");
        body.append(textarea);

        $(".message-control-container").each(function(i, x) {
            x = $(x);
            x.html("");
        });

        var controls = $(".message-controls").first().clone();

        controlContainer.append(controls);

        textarea.focus();
        textareaHeight = textarea[0].scrollHeight;
        textarea.css("minHeight", `${textareaHeight}px`);
    };

    SessionMessage.fnCancelEdit = function()
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

    SessionMessage.fnSave = function(e)
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
            url: `/v1/session/${Session.fnGetName()}/message/${id}/save`,
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
                    SessionMessage.fnCancelEdit();
                }
            }
        });
    };

    SessionMessage.fnHide = function(e, hidden)
    {
        e = $(e);
        var parent = e.parents(".message-wrapper").first();
        var id = parent.find(".message-id")
            .first()
            .html()
            .trim();

        $.ajax({
            url: `/v1/session/${Session.fnGetName()}/message/${id}/save`,
            type: "POST",
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify({ hidden: hidden }),
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

    SessionMessage.fnDelete = function(e)
    {
        e = $(e);
        var parent = e.parents(".message-wrapper").first();
        var id = parent.find(".message-id")
            .first()
            .html()
            .trim();

        $.ajax({
            url: `/v1/session/${Session.fnGetName()}/message/${id}/delete`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                session_name: Session.fnGetName()
            }),
            success: function(data)
            {
                if (data.deleted)
                    parent.remove();
            }
        });
    };
}); 
