/*global jQuery: false, document: false, alert: false, console: false */
(function ($) {
    "use strict";

    function load_model(model_id) {

        if (model_id === undefined) {
            model_id = $("#left_column").find("a").first().attr('id');
        }

        $.getJSON('/model/', {model: model_id}, function (response) {
            var table, field, elem, item, record, ul;

            $("#model_table").remove();

            table = $('<table id="model_table">');
            table.append('<thead><tr>').append('<tbody>');

            for (field in response.fields) {
                if (response.fields.hasOwnProperty(field)) {
                    elem = $('<th>').addClass(response.fields[field][2]).text(response.fields[field][0]);
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
            $("#right_column").prepend(table);

            ul = $("#new_record").empty();

            for (field in response.fields) {
                if (response.fields.hasOwnProperty(field)) {
                    if (response.fields[field][1] !== 'id') {
                        elem = $('<li><label for="input-' + response.fields[field][1] + '">' + response.fields[field][0] + ':</label><input id="input-' + response.fields[field][1] + '"></li>');
                        ul.append(elem);
                    }
                }
            }

            console.log(response);
        });
    }

    load_model();

    $("a").click(function () {
        $(".selected").removeClass("selected");
        $(this).parent().addClass("selected");
        load_model(this.id);
    });

}(jQuery));