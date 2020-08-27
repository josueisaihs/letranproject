$(document).ready(()=>{
    AOS.init();

    $(".navbar-brand").hide();

    valueTop($(window));

    $(window).scroll(()=>{
        valueTop(this);
    });    

    $(".menu-nav").on('click', function(event) {
        if (this.hash !== "") {
          event.preventDefault();
          
          var hash = this.hash;

          $(".navbar-nav .nav-item .active").removeClass("active");
          $(this).addClass("active");
          
          const top = hash === "#inicio" ? $(hash).offset().top : $(hash).offset().top - $(".navbar-nav").height(); 

          $([document.documentElement, document.body]).animate({
            scrollTop: top
          }, {duration: 1000, easing: 'swing'});
        }  // End if
    });
    
    $("#noticias").waypoint((direction)=>{
        if(direction === "down"){
            $('.counter').each(function () {
                $(this).prop('Counter', 0).animate({
                    Counter: $(this).text()
                }, {
                    duration: 4000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now));
                    }
                });
            },
            {
                offset: "-25%",
            });
        } 
    }); 
    
    
    $("#id_suscribirse").on("submit", (e)=>{
        e.preventDefault();
        const url = $("#id_suscribirse").attr("data-url");
        const email = $("#id_email").val();
        if (validarEmail(email)){
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    email: email
                },
                success: function (response) {
                    if (response.Exito === 'True'){
                        toastSuccess.show();   
                        $("#id_email").val("");
                    }else{
                        $(".toast-error-text").html("Ya existe su cuenta de correo");
                        toastError.show();
                    }      
                },
                error: (xhr, errmsg, err)=>{
                    $(".toast-error-text").html("Compruebe su conexión a internet");
                    toastError.show();
                }
            });
        }else{
            $(".toast-error-text").html("Su dirección de correo no es válida");
            toastError.show();
        }
    });

    try {
        var toastError = new bootstrap.Toast(document.getElementById("id_toastError"), 'autohide');
        var toastSuccess = new bootstrap.Toast(document.getElementById("id_toastSuccess"), 'autohide');
    } catch (error) {
        
    }
    

    $(".cursos .nav-item .nav-link").click(function() {
        $(".cursos .nav-item .activo").map((iter, el)=>{
            $(el).removeClass("link-primary border-bottom border-primary activo").addClass("link-secondary");
        });

        $(this).addClass("link-primary border-bottom border-primary activo").removeClass("link-secondary");        

        filtroCursos();
    });

    try {
        filtroCursos();
    } catch (error) {
        
    }   
    
    try{
    $(".enlace-card").hide();
    getPreview($(".enlace").attr('href'))
    } catch(errr){}
});

function valueTop(element){
    const isMobile = {
        Android: function() {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function() {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function() {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function() {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function() {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function() {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    };

    if ($(element).scrollTop() > 50){
        $(".navbar").addClass("bg-dark shadow").removeClass("bg-transparent");
        $(".navbar-brand").show();
        
        if (isMobile.any()){
            $(".navbar-nav").addClass("navbar-nav-trans").removeClass("bg-dark");
        }
    }else{
        $(".navbar").addClass("bg-transparent").removeClass("bg-dark shadow");
        $(".navbar-brand").hide();
        
        if (isMobile.any()){
            $(".navbar-nav").removeClass("navbar-nav-trans").addClass("bg-dark");
        }
    }
}

function validarEmail(valor) {
  if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/.test(valor)){   
    return true
  } else {
   return false
  }
}

function filtroCursos(){
    const activo = $(".cursos .nav-item .activo").html().toString().toLowerCase();
    
    $(".curso-contenedor").map((iter, el)=>{
        if ($(el).attr("data-course").toString().toLowerCase().indexOf(activo) > -1){
            $(el).show();
        }else{
            $(el).hide();
        }
    });
}

function getPreview(externalUrl){
    var target = externalUrl;

    // $.ajax({
    //     url: "https://api.linkpreview.net",
    //     dataType: 'json',
    //     data: {q: target, key: 'ff55066756cdd0c5f063bd3c7d33c138'},
    //     success: function (data) {
    //         $(".enlace-title").html(data.title);
    //         $(".enlace-url").html(data.url);
    //         $(".enlace-img").attr("src", data.image);
    //         $(".enlace-card").show("slow");
    //     }
    // });

    $.ajax({
        url: url.urlApi,
        type: "POST",
        dataType: 'json',
        data: {q: target,},
        success: function(data){
            $(".enlace-title").html(data.title);
            $(".enlace-url").html(data.url);
            $(".enlace-img").attr("src", data.image);
            $(".enlace-card").show("slow");
        }
    });
}