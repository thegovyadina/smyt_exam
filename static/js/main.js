/*global jQuery: false, document: false, alert: false, console: false */
(function ($) {
    "use strict";

    function getCookie(name) {
        var cookieValue = null, cookies, i, cookie;
        if (document.cookie && document.cookie !== '') {
            cookies = document.cookie.split(';');
            for (i = 0; i < cookies.length; i += 1) {
                cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

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
                        elem = $('<li><label for="input-' + response.fields[field][1] + '">'
                            + response.fields[field][0] + ':</label><input class="new_record_input" data-type="' + response.fields[field][2]
                            + '" id="input-' + response.fields[field][1] + '"></li>');
                        ul.append(elem);
                    }
                }
            }

            console.log(response);
        });
    }

    function validate_record() {
        var data = {}, i, fields = $("input.new_record_input"), input, value, type, name;
        $('.invalid').removeClass('invalid');

        // TODO: remove for...in everywhere
        for (i = 0; i < fields.length; i += 1) {
            input = $(fields[i]);
            name = input.attr('id').split('-')[1];
            value = input.val();
            type = input.data('type');

            if ((type === 'integerfield') && (isNaN(value))) {
                $('#input-' + name).addClass('invalid');
                alert('Значение должно быть числом.');
                return false;
            }

            if ((type === 'datefield') && false) {
                $('#input-' + type).addClass('invalid');
                alert('Значение должно быть датой.');
                return false;
            }

            data[name] = {
                value: value,
                type: type
            };
        }
        return data;
    }

    load_model();

    $("a").click(function () {
        $(".selected").removeClass("selected");
        $(this).parent().addClass("selected");
        load_model(this.id);
    });

    $('#return').click(function () {
        var data = validate_record();

        if (!data) {
            return;
        }

        $.post('/model/', {'csrfmiddlewaretoken': csrftoken, data: data}, function () {
            var model_id = $(".selected")[0].attr('class');
            $("input").empty();
            load_model(model_id);
        }, 'json');
    });

}(jQuery));