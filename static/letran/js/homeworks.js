$(document).ready(function () {
    document.querySelectorAll('.btn').forEach(element => {
        
        $(element).click(function (e) { 
            $(element).prop("disabled", true)
            let spinner = $(element).find($(".spinner-grow"))[0]
            $(spinner).removeClass('invisible')
            $.ajax({
                type: "post",
                url: urldelete,
                data: {'slug': $(element).attr('data-slug')},
                success: function (response) {
                    location.reload()
                },
                error: (xhr, errmsg, err)=>{
                    console.log(err, errmsg);
                    $(element).prop("disabled", false)
                    $(spinner).addClass('invisible')
                }
            });
        });
    })
});