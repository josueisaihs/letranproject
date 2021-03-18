$(document).ready(function () {
    var toastSuccess = new bootstrap.Toast(document.getElementById("id_toast"), 'autohide');
    document.querySelectorAll('.form-control').forEach(element => {
        $(element).change((e)=>{
            const nota = $(element).val();
            const pk = $(element).attr('data-enrollment');
             console.log("Enviando...")
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