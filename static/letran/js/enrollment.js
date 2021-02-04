$(document).ready(function () {
    $("#continuar").prop('disabled', true)

    $(".form-check-input").change(function (e) { 
        e.preventDefault();
        subject = $(this).attr('data-subject')
        credict = Number($(this).attr('data-etcs'))

        total = Number($("#totalSubj").html())
        etcs = Number($("#totalEtcs").html())

        if ($(this).prop('checked')){
            total += 1
            etcs += credict
        }else{
            if (total > 0){
                total -= 1
            }

            if (etcs - credict >= 0){
                etcs -=credict
            }
        }
        
        $("#totalSubj").html(total)
        $("#totalEtcs").html(etcs)

        
        $("#continuar").prop('disabled', total == 0)
    });

    // todo: Terminar que los cursos elegidos se envíen por post al Enrollment y continuar a la siguiente página
    $.ajax({
        type: "POST",
        url: "url",
        data: "data",
        dataType: "dataType",
        success: function (response) {
            
        }
    });
});