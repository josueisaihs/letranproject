$(document).ready(()=>{
    
    $("#id_buscar").on('keyup', ()=>{
        $(".course-name").map((iter, value)=>{
            const txt = $("#id_buscar").val().toString().toLowerCase();
            if($(value).html().toString().toLowerCase().indexOf(txt) > -1)
                $(value).parent().show();
            else
                $(value).parent().hide();
        });
    });

});

function eliminarApp(){
    const pk = $("#id_aplicar_delete_modal").attr("data-app");
    $.ajax({
        url: urls.delete,
        type: "POST",
        data: {
            app: pk,
        },
        success: function(json){
            if (json.Exito === 'True'){
                location.reload(true);
            }
            else{
                console.log("Error")
            }                        
        },
        error: function(xhr, errmsg, err){
            console.log(errmsg, err);
        }
    });
}

function cancelarApp(){
    const pk = $("#id_aplicar_cancel_modal").attr("data-app");
    $.ajax({
        url: urls.cancel,
        type: "POST",
        data: {
            app: pk,
        },
        success: function(json){
            if (json.Exito === 'True'){
                location.reload(true);
            }
            else{
                console.log("Error")
            }                        
        },
        error: function(xhr, errmsg, err){
            console.log(errmsg, err);
        }
    });
}