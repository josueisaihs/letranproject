{% load static %}

$(document).ready(()=>{
    console.log("{{ user.username }}");
    {% if user.is_authenticated %}
        $("#name").val("{% if user.name %}{{ user.username }} {{ user.lastname }}{% else %}{{ user.username }}{% endif %}");
        $("#email").val("{{ user.email }}");
    {% endif %}
});

$("#buttonSend").on("click", function(e){
    e.preventDefault();

    $.ajax({
        url: "{% url 'view_index_contact_send' %}",
        type: "POST",
        data: {
            name: $("#name").val(),
            email: $("#email").val(),
            message: $("#message").val()
        },
        success: function (json) {
            if (json.data === 'True'){
                $("#name").val("");
                $("#email").val("");
                $("#message").val("");
            }       
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg, err);
        }
    });    
});