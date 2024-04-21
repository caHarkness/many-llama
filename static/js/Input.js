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
                    if (x.prop("tagName") == "INPUT")
                        if (x.attr("type").toLowerCase() == "checkbox")
                        {
                            value = x.is(":checked");
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
                    value = parseInt(value);

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

            if (input.length > 0)
            {

                while (true)
                {
                    input = input.first();

                    if (input.prop("tagName") === "INPUT")
                        if (input.attr("type").toLowerCase() == "checkbox")
                        {
                            input.prop("checked", value);
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
