$(document).ready(function () {
    var toastSuccess = new bootstrap.Toast(document.getElementById("id_toast"), 'autohide');
    document.querySelectorAll('.form-select').forEach(element => {
        $(element).change((e)=>{
            var optionSelected = $(element).find("option:selected");
            var valueSelected  = optionSelected.val();
            const hwpk = $(element).attr('data-hw');

            $.ajax({
                type: "POST",
                url: urlnote,
                data: {'hw': hwpk, 'note': valueSelected},
                success: function (response) {
                    if (response.response){
                        toastSuccess.show()
                    }
                },
                error: (xhr, errmsg, err)=>{
                    console.log(err, errmsg);
                }
            });
        });
    });    
});