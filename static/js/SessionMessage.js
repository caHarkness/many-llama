$(function() {
    SessionMessage = {};
    SessionMessage.fnEdit = function(e)
    {
        e = $(e);

        var parent = e.parents(".message-template-instance").first();
        var controlContainer = parent.find(".message-control-container").first();

        SessionMessage.fnCancelEdit();

        var body = parent.find("[name='body']").first();
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

        controls.find(".favorite-message-btn").first().addClass("d-none");
        controls.find(".unfavorite-message-btn").first().addClass("d-none");
        controls.find(".hide-message-btn").first().addClass("d-none");
        controls.find(".unhide-message-btn").first().addClass("d-none");

        var isFavorite = parseInt(parent.find("[name='favorite']").first().html()) == 1;
        var isHidden = parseInt(parent.find("[name='hidden']").first().html()) == 1;

        if (isFavorite)
                controls.find(".unfavorite-message-btn").first().removeClass("d-none");
        else    controls.find(".favorite-message-btn").first().removeClass("d-none");

        if (isHidden)
                controls.find(".unhide-message-btn").first().removeClass("d-none");
        else    controls.find(".hide-message-btn").first().removeClass("d-none");

        controlContainer.append(controls);

        textarea.focus();
        textareaHeight = textarea[0].scrollHeight;
        textarea.css("minHeight", `${textareaHeight}px`);
    };

    SessionMessage.fnCancelEdit = function()
    {
        $(".message-template-instance").each(function(i, x) {
            x = $(x);
            var body = x.find("[name='body']").first();
            body.removeClass("w-75");

            var textarea = body.find("textarea");
            if (textarea.length > 0)
            {
                textarea = textarea.first();
                var textareaText = textarea.val();
                //body.html(textareaText);
                body.html(x.find("[name='body_original']").html());
            }

            x.find(".message-control-container")
                .first()
                .html("");
        });
    };

    SessionMessage.fnSave = function(e)
    {
        e = $(e);
        var parent = e.parents(".message-template-instance").first();
        var id = parent.find("[name='id']")
            .first()
            .html()
            .trim();

        var textarea = parent.find("[name='body'] textarea");

        if (textarea.length < 1)
            return;

        textarea = textarea.first();
        textareaText = textarea.val();

        $.ajax({
            url: `/v1/session/${Session.fnGetName()}/message/${id}`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({ body: textareaText }),
            success: function(response)
            {
                if (response.success)
                {
                    parent.find("[name='body_original']").html(textareaText);
                    SessionMessage.fnCancelEdit();
                }
            }
        });
    };

    SessionMessage.fnFavorite = function(e, favorite)
    {
        e = $(e);
        var parent = e.parents(".message-template-instance").first();
        var id = parent.find("[name='id']")
            .first()
            .html()
            .trim();

        $.ajax({
            url: `/v1/session/${Session.fnGetName()}/message/${id}`,
            type: "POST",
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify({ favorite: favorite }),
            success: function(response)
            {
                if (response.success)
                {
                    parent.find(".favorite-message-btn").first().addClass("d-none");
                    parent.find(".unfavorite-message-btn").first().addClass("d-none");

                    if (favorite)
                            parent.find(".unfavorite-message-btn").first().removeClass("d-none");
                    else    parent.find(".favorite-message-btn").first().removeClass("d-none");
                }
            }
        });
    };

    SessionMessage.fnHide = function(e, hidden)
    {
        e = $(e);
        var parent = e.parents(".message-template-instance").first();
        var id = parent.find("[name='id']")
            .first()
            .html()
            .trim();

        $.ajax({
            url: `/v1/session/${Session.fnGetName()}/message/${id}`,
            type: "POST",
            headers: { "Content-Type": "application/json" },
            data: JSON.stringify({ hidden: hidden }),
            success: function(response)
            {
                if (response.success)
                {
                    parent.removeClass("hidden-message opacity-50");
                    parent.find(".hide-message-btn").first().addClass("d-none");
                    parent.find(".unhide-message-btn").first().addClass("d-none");

                    if (hidden)
                    {
                        parent.addClass("hidden-message opacity-50");
                        parent.find(".unhide-message-btn").first().removeClass("d-none");
                    }

                    else
                    {
                        parent.find(".hide-message-btn").first().removeClass("d-none");
                    }

                }
            }
        });
    };

    SessionMessage.fnDelete = function(e)
    {
        e = $(e);
        var parent = e.parents(".message-template-instance").first();
        var id = parent.find("[name='id']")
            .first()
            .html()
            .trim();

        $.ajax({
            url: `/v1/session/${Session.fnGetName()}/message/${id}`,
            type: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({ delete: true }),
            success: function(response)
            {
                if (response.success)
                    parent.remove();
            }
        });
    };
}); 
