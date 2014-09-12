/*global jQuery: false, document: false, alert: false, console: false */
(function ($) {
    "use strict";

    $("a").click(function () {
        $.getJSON('/get_model/', {model: this.id}, function (response) {
            console.log(response);
        });
    });

}(jQuery));