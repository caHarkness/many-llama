$(function() {
    FormValidator = {};

    FormValidator.getInputs = function()
    {
        return $("*[fv-regex]");
    };

    // Compatibility for jquery-styled event registrations:
    FormValidator.on = function(str, callback, extra = null)
    {
        switch (str)
        {
            case "pass":
                FormValidator.onPass(callback);
                break;

            case "confirm":
                FormValidator.onConfirm(callback, extra);
                break;

            default:
                console.log("Unhandled event '" + str + "'");
        }
    };

    FormValidator.onPass = function(callback)
    {
        var pass = 1;

        FormValidator.getInputs().each(function(i, x) {
            if (pass == 0)
                return;

            x = $(x);

            var tagStr          = x.get(0).tagName.toLowerCase();
            var regexStr        = x.attr("fv-regex");
            var warningStr      = x.attr("fv-warning");
            var targetStr       = x.attr("fv-target");
            var classStr        = x.attr("fv-class");
            var evalStr         = null;

            // If no failure class is specified, use Bootstrap's .border-danger:
            if (classStr == null || classStr.length < 1)
                classStr = "border-danger";

            // If no failure message is specified, use a generic message:
            if (warningStr == null || warningStr.length < 1)
                warningStr = "Please correct the highlighted input and try again";

            if (tagStr == "input")
                evalStr = x.val();

            if (tagStr == "textarea")
                evalStr = x.val();

            // Change the classes of a different element if the fail target is specified:
            if (targetStr !== null && typeof targetStr === "string" && targetStr.length > 0)
                x = $(targetStr);

            var regexObj = new RegExp(regexStr, "g");

            if (!evalStr.match(regexObj))
            {
                x.addClass(classStr);
                x.focus();
                x.select();
                console.error(warningStr);

                pass = 0;
                return;
            }

            x.removeClass(classStr);
        });

        if (pass == 1)
            if (typeof callback === "function")
                callback();
    };

    FormValidator.onConfirm = function(callback, id)
    {
        if (typeof(FormValidator.clickCount) !== "object")
            FormValidator.clickCount = {};

        if (!(id in FormValidator.clickCount))
            FormValidator.clickCount[id] = 3;

        if (FormValidator.clickCount[id] > 1)
        {
            FormValidator.clickCount[id]--;
            console.error(`Click ${FormValidator.clickCount[id]} more time(s) to do this`);
            return;
        }

        if (typeof(callback) === "function")
            callback();
    };

    if (FormValidator.getInputs().length > 0)
        console.log("This page uses form validation via formvalidator.js");
});
