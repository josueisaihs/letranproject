
function sendMail(el){
    const courseslug = $("#sendmail_course option:selected").val().toString();
    const subject = $("#sendmail_subject").val().toString();
    const body = $("#sendmail_body").val().toString();

    $(el).prop("disabled", true);
    $(el).children("div.spinner-border").removeClass("invisible");

    if (courseslug !== "none" && subject.length > 5 && body.length > 15){
        $.ajax({
            type: "post",
            url: comunicadourl, 
            data: {"courseslug": courseslug, "subject": subject, "body": body},
            success: function (response) {
                if (response.response){
                    console.log("OK");
                    $(el).prop("disabled", false);
                    $(el).children("div.spinner-border").addClass("invisible");
                    console.log("Todo ok")

                    $("#sendmail_subject").val("")
                    $("#sendmail_body").val("")
                }
            },
            error: (xhr, errmsg, err)=>{
                console.log("ERROR", errmsg.toString(), err.toString());
            }
        });
    }else{
        $(el).prop("disabled", false);
        $(el).children("div.spinner-border").addClass("invisible");
        console.log("Todo ok")
    }
}