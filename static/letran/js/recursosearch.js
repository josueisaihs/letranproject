$(document).ready(function () {
    $(".form-control").on("keydown", ()=>{
        const txt = $(".form-control").val().toString().toLowerCase()
        console.log(txt)
        document.querySelectorAll(".recourse-container").forEach(el => {
            const name = $(el).attr("data-name")
            if (name !== ""){
                if (name.toString().toLowerCase().indexOf(txt) > -1) 
                    $(el).show()
                else 
                    $(el).hide()
            }else{
                $(el).show()
            }
            
        })
    })
});