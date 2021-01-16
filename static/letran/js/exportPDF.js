// import { jsPDF } from "jspdf";

$(document).ready(function () {
    $('#exportpdf').click((e)=>{
        var pdf = new jsPDF('p', 'pt', 'letter');
        const source = $(".ckeditor")[0]

        const specialElementHandlers = {
            '#bypassme': function (element, renderer) {
                return true
            }
        };
        const margins = {
            top: 80,
            bottom: 60,
            left: 40,
            width: 522
        };

        pdf.fromHTML(
            source, 
            margins.left, // x coord
            margins.top, { // y coord
                'width': margins.width, 
                'elementHandlers': specialElementHandlers
            },

            function (dispose) {
                pdf.save('Prueba.pdf');
            }, margins
        );
    });
});