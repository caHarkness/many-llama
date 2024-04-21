$(function() {
    SessionPage = {};

    SessionPage.fnClearSearch = function()
    {
        $("[name='search-text']")
            .first()
            .val("")
            .trigger("input");
    };

    SessionPage.fnSettingsModal = function()
    {
        Input.fnSetValues("#settings-modal", Session.data);

        $("#settings-modal")
            .modal("show");

        Input.fnSetTextareaHeight();
    };

    SessionPage.fnAddMessage = function(m, append = true)
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

        if (append)
            $("#messages").first().append(div);

        return div;
    };

    SessionPage.fnShowAll = function()
    {
        $(".hidden-message").removeClass("d-none");
    };

    SessionPage.fnEdit = function()
    {
        SessionPage.fnShowAll();
        $(".message-control-link").removeClass("d-none");
    };

    SessionPage.fnBind = function()
    {
        $(document).unbind("keyup");
        $(document).on("keyup", function(e) {
            if (e.keyCode == 13)
                if ($("[name='user-input']").is(":focus"))
                    Session.fnSend();
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

    SessionPage.fnBind();
});
