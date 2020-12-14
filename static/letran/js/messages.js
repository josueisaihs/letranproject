$(document).ready(function () {
    update_msg();
    setInterval(update_msg, 5000);

    $("#id_msg_send").click(()=>{
        const msg = $("#id_msg")
        .val()
        .toString()
        .trim()
        .replace(/pinga|comepinga|maricon|puta/gi, 
            (x)=>{
                return "*".repeat(x.length);
            }
        );

        const d = new Date().toLocaleString();

        update_msg();      

        $.ajax({
            type: "POST",
            url: sendmsg,
            data: {
                subjectslug: subject,
                msg: msg
            },
            success: function (response) {
                console.log(response.slug)
                $("#id_msg_pool").append(
                    `<div class="rounded bg-info my-1 ml-3 p-1">
                        <span class="text-white">${msg}</span>
                        <br>
                        <span class="text-secondary">
                            ${d}
                        </span>
                        <span class="float-right"><a href="#" class="link-dark">
                        <i class="fas fa-times"></i> Eliminar</a></span>
                    </div> `
                );
            }
        });

        $("#id_msg").val("");
    });

    function update_msg() {
        $.ajax({
            type: "POST",
            url: updatemsg,
            data: {subjectslug: subject,},
            success: function (response) {
                const colors = ['text-warning', 'text-info', 'text-white-50', 'text-success']
                const mcolor = colors[Math.floor(Math.random() * colors.length)];

                $("#id_msg_pool").empty();
                JSON.parse(response.data).forEach(element => {
                    if (element.fields.user === userpk){
                        $("#id_msg_pool").append(
                            `<div class="rounded bg-info my-1 ml-3 p-1">
                                <span class="text-white">${element.fields.body}</span>
                                <br>
                                <span class="text-secondary">
                                    ${element.fields.createdate}
                                </span>
                                <span class="float-right"><a href="#" onclick="eliminar('${element.fields.slug}')" class="link-dark">
                                <i class="fas fa-times"></i> Eliminar</a></span>
                            </div> `
                        );
                    } else {
                        $.ajax({
                            type: "POST",
                            url: usermsg,
                            data: {userpk: element.fields.user},
                            success: function (response) {
                                $(`#${element.fields.slug}-user`).html(response.response);
                            }
                        });

                        $("#id_msg_pool").append(
                            `<div class="rounded bg-dark my-1 mr-3 p-1">
                                <span><i class="${mcolor}"></i> <span id="${element.fields.slug}-user" class="${mcolor}"><i>Esperando...</i></span></span>
                            <br>
                            <span class="text-white">${element.fields.body}
                            </span>
                            <br>
                            <span class="text-secondary">
                                ${element.fields.createdate}
                            </span>
                        </div>`);                 
                    }
                });
            }
        });
    }

    
});

function eliminar(slug){
    $.ajax({
        type: "POST",
        url: deletemsg,
        data: {
            slug: slug
        },
        success: function (response) {
            // update_msg();
        }
    });
}