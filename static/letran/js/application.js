$(document).ready(()=>{
    AOS.init();

    document.getElementById("id_error").style.display = "none";

    $("#id_send").on("click", function(e){
        e.preventDefault();

        let asks = [];

        const askselects = $(".ask-select");
        const asktextareas = $(".ask-textarea");
        const askradio = $(".ask-radio");

        let enviarForm = true;

        askselects.map(function(iter, ask){
            if ($(ask).val() != 0){
                asks.push([$(ask).attr("data-ask"), "o", $(ask).val()]);
            }else{
                $(ask).addClass("is-invalid");
                enviarForm = false;

            }
        });

        asktextareas.map(function(iter, ask){
            if ($(ask).val().length > 19){
                asks.push([$(ask).attr("data-ask"), "t", $(ask).val()]);
            }else{
                $(ask).addClass("is-invalid");
                enviarForm = false;
            }
        });

        askradio.map(function(iter, ask){
            const pk = $(ask).attr("data-ask");
            const radioValue = $("input[name='radio_" + pk + "']:checked").val();
            asks.push([$(ask).attr("data-ask"), "r", radioValue]);
        });

        if (enviarForm){
            asks.map(function (ask, iter){
                $.ajax({
                    url: url.urlApi,
                    type: "POST",
                    data: {
                        ask: ask[0],
                        askType: ask[1],
                        answer: ask[2]
                    },
                    success: function(json){
                        if (json.Exito === 'True'){
                            console.log("OK");
                            window.location.replace(url.urlRes);
                        }
                        else{
                            document.getElementById("id_error").innerHTML = "Error interno. Por favor, espere un tiempo y vuelva a intentar.";                            
                            document.getElementById("id_error").style.display = "block";
                        }                        
                    },
                    error: function(xhr, errmsg, err){
                        console.log(errmsg, err);
                        document.getElementById("id_error").innerHTML = "Error de conexión. Revise su conexión de internet";
                        document.getElementById("id_error").style.display = "block";
                    }
                });
            });
        } else{
            document.getElementById("id_error").innerHTML = "Complete los campos requeridos.";
            document.getElementById("id_error").style.display = "block";
            $("html, body").animate({scrollTop: 0}, 1000);
        }      
    });
});