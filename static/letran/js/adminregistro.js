$(document).ready(function () {
    var toastSuccess = new bootstrap.Toast(document.getElementById("id_toast"), 'autohide');

    document.querySelectorAll('.form-check-input').forEach(element=>{
        $(element).change(e=>{
            const form_control = $(element).parent().children('.form-control')
            $(form_control).prop('disabled', !$(element).prop('checked'))            
        })
    })

    document.querySelectorAll('.form-control').forEach(element => {
        $(element).change((e)=>{
            const nota = $(element).val();
            const pk = $(element).attr('data-enrollment');
            $.ajax({
                type: "post",
                url: urlnote,
                data:  {'enrollment': pk, 'note': nota},
                success: function (response) {
                    if (response.response){
                        toastSuccess.show()
                    }
                },
                error: (xhr, errmsg, err)=>{
                    console.log(err, errmsg);
                }
            });
        })
    });
});