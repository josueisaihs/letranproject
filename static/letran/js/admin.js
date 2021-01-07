$(document).ready(()=>{

    $('#updatecomments').on('click', ()=>{
        var textarea = document.querySelector('comments')
        const text = `${textarea.html()} Última Actualización:${textarea.getAttribute('data-teacher')}`
        const pk = textarea.getAttribute('data-app')
        
        $.ajax({
            url: urls.accion,
            type: "POST",
            data: {
                app: pk,
                comment: text
            },
            success: function(json){
                if (json.Exito === 'True'){
                    textarea.html(text)
                }else{
                    console.log("Error");
                }
            },
            error: function(xhr, errmsg, err){
                console.log(errmsg, err);
            }
        });
    })
    
    $("#id_buscar").on('keyup', ()=>{
        const txt = $("#id_buscar").val().toString().toLowerCase();

        $(".course-name").map((iter, value)=>{            
            if($(value).html().toString().toLowerCase().indexOf(txt) > -1)
                $(value).parent().attr("data-show", 1);
            else
                $(value).parent().attr("data-show", 0);
        });

        $(".app-student").map((iter, value)=>{            
            if($(value).html().toString().toLowerCase().indexOf(txt) > -1){
                $(value).parent().show();
                $(value).parent().attr("data-show", 1);
            }else{
                if ($(value).parent().attr("data-show") != 1){
                    $(value).parent().attr("data-show", 0);
                    $(value).parent().hide();
                }
            }
        });
    });
    

    $("#id_status_filtro button").click(function() {
        const txt = $(this).text() === "Todos" ? "" : $(this).text().toString().toLowerCase();
        $(this).addClass("active").siblings().removeClass('active');
        $(".app-status").map((iter, value)=>{
            if($(value).html().toString().toLowerCase().indexOf(txt) > -1)
                $(value).parent().show();
            else
                $(value).parent().hide();
        });
    });

    tippy('#id_btn_list', {
        content: 'Vista Lista',
        delay: [500, 250],
        animation:'shift-away',
        inertia: true,
        animateFill: true,
    });

    tippy('#id_btn_detail', {
        content: 'Vista Detalle',
        delay: [500, 250],
        animation:'shift-away',
        inertia: true,
        animateFill: true,
    });

    tippy('.procesar', {
        content: 'Preseleccionar al aspirante (Entrevista)',
        delay: [500, 250],
        animation:'shift-away',
        inertia: true,
        animateFill: true,
    });
});

function eliminar(){
    const pk = $("#id_eliminar_btn").attr("data-app");
    $.ajax({
        url: urls.delete,
        type: "POST",
        data: {
            app: pk,
        },
        success: function(json){
            if (json.Exito === 'True'){
                location.reload();
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

function accion(){
    const pk = $("#id_accion_btn").attr("data-app");
    const accion = $("#id_accion_btn").attr("data-accion");

    $.ajax({
        url: urls.accion,
        type: "POST",
        data: {
            app: pk,
            status: accion
        },
        success: function(json){
            if (json.Exito === 'True'){
                location.reload();
            }else{
                console.log("Error");
            }
        },
        error: function(xhr, errmsg, err){
            console.log(errmsg, err);
        }
    });
}

function accion(){
    const pk = $("#id_accion_btn").attr("data-app");
    const accion = $("#id_accion_btn").attr("data-accion");

    $.ajax({
        url: urls.accion,
        type: "POST",
        data: {
            app: pk,
            status: accion
        },
        success: function(json){
            if (json.Exito === 'True'){
                location.reload();
            }else{
                console.log("Error");
            }
        },
        error: function(xhr, errmsg, err){
            console.log(errmsg, err);
        }
    });
}