$(document).ready(function () {
    document.querySelectorAll('.btn').forEach(element => {
        $(element).click(function (e) { 
            
            $.ajax({
                type: "post",
                url: urldelete,
                data: {'slug': $(element).attr('data-slug')},
                success: function (response) {
                    location.reload()
                }
            });
        });
    })
});