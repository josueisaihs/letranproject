$(document).ready(()=>{
    AOS.init();

    $("#id_aceptar").addClass("disabled");
    
    $("#id_checked").on("change", ()=>{
        if ( $("#id_checked")[0].checked )
            $("#id_aceptar").removeClass("disabled");
        else
            $("#id_aceptar").addClass("disabled");
    });
});