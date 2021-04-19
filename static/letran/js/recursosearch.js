$(document).ready(function () {
    $(".form-control").on("change", ()=>{
        const txt = $(".form-control").val().toString().toLowerCase()
        document.querySelectorAll(".recourse-container").forEach(el => {
            const name = $(el).attr("data-name")
            if (name.toString().toLowerCase().indexOf(txt) > -1) 
                $(el).show()
            else 
                $(el).hide()
        })
    })
});