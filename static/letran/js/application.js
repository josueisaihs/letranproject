$(document).ready(()=>{
    AOS.init();

    document.getElementById("id_error").style.display = "none";

    $("#id_send").on("click", (e)=>{
        e.preventDefault();

        $("#id_send").prop("disabled", true);
        $(".spinner-border").removeClass("invisible");
        $(".btn-text").html("Validando ...")

        let asks = [];

        const askselects = $(".ask-select");
        const asktextareas = $(".ask-textarea");
        const askradio = $(".ask-radio");
        const askcheck = $(".ask-check");

        let enviarForm = true;

        askselects.map((iter, ask)=>{
            if ($(ask).val() != 0){
                asks.push([$(ask).attr("data-ask"), "o", $(ask).val()]);
            }else{
                $(ask).addClass("is-invalid");
                enviarForm = false;

            }
        });

        asktextareas.map((iter, ask)=>{
            if ($(ask).val().length > $(ask).attr["minlength"]){
                asks.push([$(ask).attr("data-ask"), "t", $(ask).val()]);
            }else{
                $(ask).addClass("is-invalid");
                enviarForm = false;
            }
        });

        askradio.map((iter, ask)=>{
            const pk = $(ask).attr("data-ask");
            const radioValue = $("input[name='radio_" + pk + "']:checked").val();
            asks.push([$(ask).attr("data-ask"), "r", radioValue]);
        });

        askcheck.map((iter, ask)=>{
            const pk = $(ask).attr("data-ask");

            let options = []

            $("input[name='check_" + pk + "']:checked").map((iter, askop)=>{
                options.push($(askop).val())
            });            

            if (options.length > 0){
                options = options.join(";");
                asks.push([$(ask).attr("data-ask"), "c", options]);    
            } else {
                options = "0;";
                asks.push([$(ask).attr("data-ask"), "c", options]); 
            }
        });

        if (enviarForm){
            asks.map((ask, iter)=>{
                $.ajax({
                    url: url.urlApi,
                    type: "POST",
                    data: {
                        ask: ask[0],
                        askType: ask[1],
                        answer: ask[2]
                    },
                    success: (json)=>{
                        if (json.Exito === 'True'){
                            console.log("OK");                            
                            $("#id_send").hide();
                            window.location.replace(url.urlRes);
                        }
                        else{
                            document.getElementById("id_error").innerHTML = "Error interno. Por favor, espere un tiempo y vuelva a intentar.";                            
                            document.getElementById("id_error").style.display = "block";
                            $("#id_send").prop("disabled", false);
                            $(".spinner-border").addClass("invisible");
                            $(".btn-text").html("Enviar")  
                        }                
                    },
                    error: (xhr, errmsg, err)=>{
                        console.log(errmsg, err);
                        document.getElementById("id_error").innerHTML = "Error de conexión. Revise su conexión de internet";
                        document.getElementById("id_error").style.display = "block";
                        $("#id_send").prop("disabled", false);
                        $(".spinner-border").addClass("invisible");
                        $(".btn-text").html("Enviar")
                    }
                });
            });
        } else{
            document.getElementById("id_error").innerHTML = "Complete los campos requeridos.";
            document.getElementById("id_error").style.display = "block";
            $("html, body").animate({scrollTop: 0}, 1000);
            
            $("#id_send").prop("disabled", false);
            $(".spinner-border").addClass("invisible");
            $(".btn-text").html("Enviar")
        } 
    });
});