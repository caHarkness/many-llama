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

        var div = MessageTemplate.fnCreate(m);

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
        /*
        ShiftHeld = false;

        $(document).unbind("keydown");
        $(document).unbind("keyup");
        
        $(document).on(
            "keyup keydown",
            function(e)
            {
                ShiftHeld = e.shiftKey;
            });
        */

        // Unused for now, we're sticking with input over textarea:
        /*
        $("[name='user-input']").on("input", function(e) {
            var input = $("[name='user-input']").first();
            input.css("minHeight", "0px");

            // var newHeight = input[0].scrollHeight +
            //    parseInt(input.css("paddingTop")) +
            //    parseInt(input.css("paddingBottom")) +
            //    "px";

            var newHeight = (input[0].scrollHeight + 4) + "px";

            input.css("minHeight", newHeight);

            $("#bottom-user-input-spacing").css(
                "height",
                $("#bottom-user-input-container").height() + "px");
        });
        */

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
