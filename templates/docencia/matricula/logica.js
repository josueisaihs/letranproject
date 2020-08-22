function readFile(input) {
    if (input.files && input.files[0]){
        var reader = new FileReader();
        reader.onload = function (e) {
            var filePreview= document.getElementById('image_preview');
            filePreview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_yearMin").change(
    function (){
        const yearMin = (new Number($("#id_yearMin").val()) + 1);
        $("#id_yearMax").attr("min", (yearMin > 10 ? yearMin : 10));
        $("#id_yearMax").val((yearMin > 10 ? yearMin : 10));
    }
);