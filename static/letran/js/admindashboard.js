function createGroup(){
    const courseslug = $("#namenewgroup").attr('data-course');
    const name = $("#namenewgroup").val()
    // const name = "Grupo A"
    console.log(name, courseslug, creategroupurl)

    if (name !== '' && courseslug !== ''){
        $.ajax({
            type: 'post',
            url: creategroupurl,
            data: {'name': name, 'course': courseslug},
            success: (response)=>{
                if (response.response){
                    location.href = urlcourse
                }else{
                    console.error("Error servidor")
                }
            },
            error: (xhr, errmsg, err)=>{
                console.error(errmsg.toString(), err.toString());
            }
        })
    }
}

function sendMail(el){
    const courseslug = $("#sendmail_subject").attr('data-course');
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

                    location.href = urlcourse
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