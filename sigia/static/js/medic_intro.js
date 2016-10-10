/**
 *    File name: medic_intro
 *    Author: Edgar Arturo Haas Pacheco
 *    Date created: 23/8/2016
 */

$(document).ready(function () {
    Date.prototype.toDateInputValue = (function () {
        var local = new Date(this);
        local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
        return local.toJSON().slice(0, 10);
    });
    $('#id_medico-date').val(new Date().toDateInputValue());
    var dt = new Date();
    var time = dt.toTimeString().split(' ')[0];
    $('#time1').val(time);
    $('.id_paciente').selectpicker();
    $('.id_paciente').selectpicker('render');
    $('.contactos').formset({
        prefix: "contacto_form",
        addText: "Agregar Contacto",
        deleteText: "Borrar",
        formCssClass: 'contactos-formset',
        deleteCssClass: 'delete-contactos-row delete-row'
    });
    $('.esto').formset({
        prefix: 'personal_form',
        formCssClass: 'esto-formset',
        deleteCssClass: 'delete-esto-row delete-row'
    });
    $('.esta').formset({
        prefix: "persona_fem_form",
        formCssClass: 'personalFem-formset',
        deleteCssClass: 'delete-personalFem-row delete-row'
    });
    $('.familia').formset({
        prefix: "family_form",
        formCssClass: 'family-formset',
        deleteCssClass: 'delete-family-row delete-row'
    });
    $('#id_medico-id_patient').change(function () {
            var num = $('#id_medico-id_patient').children("option").filter(":selected").val();
            $.ajax({
                type: 'GET',
                url: '/user/api/lista/',
                data: {
                    ids: num
                },
                contentType: 'json',
                success: function (data) {
                    var nuevo = JSON.parse(data);
                    $('#apellido').val(nuevo[1].fields.last_name);
                    $('#nombre').val(nuevo[1].fields.first_name);
                    $('#direccion').val(nuevo[0].fields.address);
                    $('#telefono').val(nuevo[0].fields.cellphone);
                    $('#cedula').val(nuevo[0].fields.id_doc_num);
                    $("#marital").val(nuevo[0].fields.marital_status);
                    if (Object.keys(nuevo).length > 2) {
                        $('#nacionalidad').val(nuevo[2].fields.name);
                        $('#canton').val(nuevo[4].fields.name);
                        $('#provincia').val(nuevo[3].fields.name);
                    } else {
                        $('#nacionalidad').val("Sin datos");
                        $('#canton').val("Sin datos");
                        $('#provincia').val("Sin datos");
                    }
                }
            });
        }
    );
    $('.panel-collapse.in').collapse('hide');
    $("#tabs").tabs();
});


