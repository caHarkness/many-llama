$(function() {
    NavbarHelper = {};

    NavbarHelper.fnInit = function()
    {
        $("#navbar-spacing-container").first().html("");
        $("#navbar-container .navbar").each(function(i, x) {
            var new_div = $("<div></div>");

            new_div.addClass("navbar-spacing");

            $("#navbar-spacing-container")
                .first()
                .append(new_div);
        });
    };

    NavbarHelper.fnInit();
});
