$(document).ready(function () {
    $("#continuar").prop('disabled', disabled)

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
    $("#continuar").on("click", function () {
        subjects = []

        document.querySelectorAll(".form-check-input").forEach(element => {            
            if ($(element).prop('checked')){
                subjects.push($(element).attr('data-subject-pk'))
            }            
        });

        $.ajax({
            type: "POST",
            url: urlenrollment,
            data: {
                "datos[]": JSON.stringify(subjects), 
                "course": course
            },
            success: function (response) {
                if (response.response){
                    console.log("Perfecto")
                    console.log(urlcourse)
                    location.href = urlcourse
                }else{
                    
                }
            },
            error: (xhr, errmsg, err)=>{
                console.log(err, errmsg);
            }
        });
    });
});