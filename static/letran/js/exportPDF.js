// import { jsPDF } from "jspdf";

$(document).ready(function () {
    $('#exportpdf').click((e)=>{
        const source = $(".ckeditor")[0]
        const classname = $(".ckeditor").attr('data-classname')

        var opt = {
            margin:       1,
            filename:     `${classname}.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2 },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' },
            pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
        };

        var worker = html2pdf().set(opt).from(source).save();
    })
});