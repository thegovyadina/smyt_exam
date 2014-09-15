/*global jQuery: false, document: false, alert: false, console: false, setTimeout: false */
(function ($) {
    "use strict";

    var load_model, save_model, csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    /* Валидация полей ввода

    @param [String] model_id - введенное значение
    @param [String] model_id - тип данных
    */
    function valid_field(value, type) {
        var  dateReg = /^\d{2}\.\d{2}\.\d{4}$/;
        if ((type === 'charfield') && (value === '')) {
            alert('Поле обязательно для заполнения.');
            return false;
        }
        if ((type === 'integerfield') && (parseInt(value, 10)).toString() !== value) {
            alert('Значение должно быть целым числом.');
            return false;
        }
        if ((type === 'datefield') && (!value.match(dateReg))) {
            alert('Значение должно быть датой в формате dd.mm.YYYY.');
            return false;
        }
        return true;
    }

    /* Создание таблицы и формсета для новой записи на основе данных модели

    @param [object] data - данные модели
    */
    function create_table(data) {
        var table, field, item, elem, record, ul;

        $("#model_table").remove();

        table = $('<table id="model_table">');

        table.append('<thead><tr>').append('<tbody>');

        for (field = 0; field < data.fields.length; field += 1) {
            elem = $('<th>').addClass(data.fields[field][2]).text(data.fields[field][0]);
            table.find('tr').append(elem);
        }

        for (item = 0; item < data.values.length; item += 1) {
            elem = $('<tr>');
            record = data.values[item];

            for (field = 0; field < record.length; field += 1) {
                elem.append('<td class="' + data.fields[field][2] + '" data-recordid="' + data.values[item][0]
                    + '" data-field="' + data.fields[field][1] + '" data-type="' + data.fields[field][2] + '">'
                    + record[field] + '</td>');
            }

            table.find('tbody').append(elem);
        }

        $("#right_column").prepend(table);

        ul = $("#new_record").empty();

        for (field = 0; field < data.fields.length; field += 1) {
            if (data.fields[field][1] !== 'id') {
                elem = $('<li><label for="input-' + data.fields[field][1] + '">'
                    + data.fields[field][0] + ':</label><input class="new_record_input" data-type="' + data.fields[field][2]
                    + '" id="input-' + data.fields[field][1] + '"></li>');
                ul.append(elem);
            }
        }

        // При клике на ячейку таблицы вставляем в нее поле ввода для редактирования значения
        $("td.charfield, td.integerfield, td.datefield").click(function () {
            var value, input_field,
                active = $(this).hasClass('active');
            if (!active) {
                $(this).addClass('active');
                value = $(this).text();
                $(this).empty();
                input_field = $('<input type="text">');
                input_field.val(value);

                // Вешаем на поле обработку нажатия Enter
                input_field.keypress(function (e) {
                    var key = e.which, model_data = {}, val = $(this).val(),
                        model_field = $(this).parent().data('field'),
                        field_type = $(this).parent().data('type'),
                        recordid = $(this).parent().data('recordid');
                    if (key === 13) {
                        $('input.active').removeClass('invalid');
                        if (!valid_field(val, field_type)) {
                            $(this).addClass('invalid');
                            return false;
                        }
                        model_data.id = recordid;
                        model_data[model_field] = val;
                        save_model(model_data);
                        return false;
                    }
                });
                $(this).append(input_field);
                input_field.focus();
            }
        });

    }

    /* Сохранение модели

    @param [object] data - данные модели
    */
    save_model = function (data) {
        var model_id = $(".selected:first").find('a').attr('id');

        if (!data) {
            return;
        }

        data.model = model_id;
        data.csrfmiddlewaretoken = csrftoken;

        $.post('/model/', data, function () {
            $("input").empty();
            load_model(model_id);
        }, 'json')
            .error(function () {
                alert('Не удалось сохранить запись');
            });
    };

    /* Получение данных модели с сервера в формате JSON

    @param [String] model_id - id модели
    */
    load_model = function (model_id) {

        if (model_id === undefined) {
            model_id = $("#left_column").find("a").first().attr('id');
        }

        $.getJSON('/model/', {model: model_id}, function (response) {
            create_table(response);
        });
    };

    load_model();

    // Обработчик клика на наименовании модели (левая колонка)
    $("a").click(function () {
        $(".selected").removeClass("selected");
        $(this).parent().addClass("selected");
        load_model(this.id);
    });

    // Обработчик клика на кнопке "Добавить"
    $('#return').click(function () {
        var data = {}, i, fields = $("input.new_record_input"),
            input, value, type, name;

        $('.invalid').removeClass('invalid');

        for (i = 0; i < fields.length; i += 1) {
            input = $(fields[i]);
            name = input.attr('id').split('-')[1];
            value = input.val();
            type = input.data('type');

            if (!valid_field(value, type)) {
                $('#input-' + name).addClass('invalid');
            }

            data[name] = value;
        }

        save_model(data);
    });

    $('body').on('focus', '#input-date_joined, .datefield input', function () {
        var that = $(this);
        $(this).datepicker({
            dateFormat: "dd.mm.yy",
            onClose: function () {
                var val = that.val(), model_data = {},
                    model_field = $(this).parent().data('field'),
                    field_type = $(this).parent().data('type'),
                    recordid = $(this).parent().data('recordid');
                if (!valid_field(val, field_type)) {
                    $(this).addClass('invalid');
                    return false;
                }
                model_data.id = recordid;
                model_data[model_field] = val;
                save_model(model_data);
            }
        });
    });

}(jQuery));