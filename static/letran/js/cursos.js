$("#id_buscar").on('keyup', ()=>{
    filtrar();
});

function filtro(el, campo) {
    $(campo).removeClass('text-primary');
    $(el).addClass('text-primary');

    filtrar();
}

function filtrar(){
    const txt = $("#id_buscar").val().toString().toLowerCase().trim();
    
    let tipo_ = $(".filtro-tipo.text-primary").html().toString().toLowerCase().trim();
    const tipo = tipo_ === "todos" ? "" : tipo_;

    let area_ = $(".filtro-area.text-primary").html().toString().toLowerCase().trim();
    const area = area_ === "todos" ? "" : area_;

    let admision_ = $(".filtro-admision.text-primary").html().toString().toLowerCase().trim();
    const admision = admision_ === "todos" ? "" : admision_;

    $(".card").map((iter, value)=>{
        const data_course = $(value).attr("data-course").toString().toLowerCase();
        const data_area = $(value).attr("data-area").toString().toLowerCase();
        const data_adminsion = $(value).attr("data-admision").toString().toLowerCase();
        const data_tipo = $(value).attr("data-tipo").toString().toLowerCase();

        console.log(data_area.indexOf(area), data_area, area);
        if (data_course.indexOf(txt) > -1 && data_area.indexOf(area) > -1 && data_adminsion.indexOf(admision) > -1 && data_tipo.indexOf(tipo) > -1)
            $(value).show();
        else
            $(value).hide();
    });
}