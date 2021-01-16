// import { jsPDF } from "jspdf";

$(document).ready(function () {
    $('#exportpdf').click((e)=>{
        const source = $(".ckeditor")[0]

        var worker = html2pdf().from(source).save();
    })
});