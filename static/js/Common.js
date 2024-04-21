$(function() {
    Common = {};
    Common.fnGetAPIHeaders = function(extras = {})
    {
        var output = {
            "Content-Type": "application/json"
        };

        if (typeof extras === "object")
            output = Object.assign({}, output, extras);

        return output;
    };
});
