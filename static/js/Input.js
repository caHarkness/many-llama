$(function() {
    Input = {};

    // Converts a jquery selector containing inputs into a key-value pair JSON object:
    Input.fnGetValues = function(selector)
    {
        output = {};

        if (typeof(selector) === "string")
            selector = $(selector);

        selector
            .first()
            .find("[name]")
            .each(function(i, x) {
                x = $(x);
                key = x.attr("name");
                value = null;

                while (true)
                {
                    if (["INPUT"].includes(x.prop("tagName")))
                        if (x.attr("type").toLowerCase() == "checkbox")
                        {
                            value = x.is(":checked");
                            break;
                        }

                    if (["DIV", "SPAN"].includes(x.prop("tagName")))
                    {
                        value = x.html();
                        break;
                    }

                    if (typeof(x.val) === "function")
                    {
                        value = x.val();
                        break;
                    }
                    
                    if (x.attr("value"))
                    {
                        value = x.attr(value);
                        break;
                    }

                    // Always exit this loop:
                    break;
                }

                if (`${value}`.match(/^-?[0-9]{1,}$/g))
                {
                    value = parseInt(value);

                    if (x.attr("data-type") == "boolean")
                    {
                        if (value == 1)
                                value = true;
                        else    value = false;
                    }
                }

                if (`${value}`.match(/^-?[0-9]{1,}(\.[0-9]{1,})?$/g))
                    value = parseFloat(value);

                if (`${value}`.length < 1)
                    value = null;

                output[key] = value;
            });

        return output;
    };

    Input.fnSetValues = function(selector, values)
    {
        if (typeof(selector) === "string")
            selector = $(selector);

        for (key in values)
        {
            var value = values[key];

            if (value == null)
                value = "";

            if (["object", "function", "undefined"].includes(typeof value))
                continue;

            var input = selector.find(`[name='${key}']`);

            console.log(input);

            if (input.length > 0)
            {
                while (true)
                {
                    input = input.first();

                    if (["INPUT"].includes(input.prop("tagName")))
                        if (input.attr("type").toLowerCase() == "checkbox")
                        {
                            input.prop("checked", value);
                            break;
                        }

                    if (typeof value === "boolean")
                    {
                        if (value)
                                value = 1;
                        else    value = 0;
                    }

                    if (["DIV", "SPAN"].includes(input.prop("tagName")))
                    {
                        input.html(value);
                        break;
                    }

                    if (typeof input.val === "function")
                    {
                        input.val(value);
                        break;
                    }

                    if (input.attr("value"))
                    {
                        input.attr("value", value);
                        break;
                    }

                    input.html(value);
                    break;
                }
            }

        }
    };

    Input.fnSetTextareaHeight = function()
    {
        $("textarea").each(function(i, x) {
            x = $(x);

            x.css("minHeight", "0px");
            x.css(
                "minHeight",
                x[0].scrollHeight +
                    parseInt(x.css("paddingTop")) +
                    parseInt(x.css("paddingBottom")) +
                    "px"
                );
        });
    };
});
