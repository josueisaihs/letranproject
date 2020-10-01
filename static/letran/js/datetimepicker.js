$(function () {
    $("#id_datepub_div").datetimepicker({
        locale: 'es',
        daysOfWeekDisabled: [0, 6],
        inline: false,
        sideBySide: true,
        enabledHours: [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        format: 'DD/MM/YYYY HH:mm',
        icons: {
            time: "fa fa-clock-o",
            date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        },
        minDate: new Date(),
        stepping: 5,
    });
});