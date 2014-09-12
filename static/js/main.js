/*global jQuery: false, document: false, alert: false, console: false */
(function ($) {
    "use strict";

    $("a").click(function () {

        $(".selected").removeClass("selected");
        $(this).parent().addClass("selected");

        $.getJSON('/get_model/', {model: this.id}, function (response) {
            var table, field, elem, item, record;

            $("#model_table").remove();

            table = $('<table id="model_table">');
            table.append('<thead><tr>').append('<tbody>');

            for (field in response.fields) {
                if (response.fields.hasOwnProperty(field)) {
                    elem = $('<th>').addClass(response.fields[field][1]).text(response.fields[field][0]);
                    table.find('tr').append(elem);
                }
            }

            for (item in response.values) {
                if (response.values.hasOwnProperty(item)) {
                    elem = $('<tr>');
                    record = response.values[item];

                    for (field in record) {
                        if (record.hasOwnProperty(field)) {
                            elem.append('<td>' + record[field] + '</td>');
                        }
                    }

                    table.find('tbody').append(elem);
                }
            }
            $(".right_column").append(table);
            console.log(response);
        });
    });

}(jQuery));