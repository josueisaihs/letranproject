Parse.initialize("UGYkYzEco5HYSHtPwAWBSmycjA9uMLAAB5dVNTmu", "r0kkbrYE9AQPKbMfnqmwvLlrdZgQ6diG3ghm5zv8"); //PASTE HERE YOUR Back4App APPLICATION ID AND YOUR JavaScript KEY
Parse.serverURL = "https://parseapi.back4app.com/";

var User = null

window.fbAsyncInit = function() {
    Parse.FacebookUtils.init({ // this line replaces FB.init({
        appId      : '445820016601305', // Facebook App ID
        cookie     : true,  // enable cookies to allow Parse to access the session
        xfbml      : true,  // initialize Facebook social plugins on the page
        version    : 'v9.0' // point to the latest Facebook Graph API version, found in FB's App dashboard.
    });

    // Put here code to run after the Facebook SDK is loaded.
    FB.AppEvents.logPageView(); 
};
(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function logIn() {
    Parse.FacebookUtils.logIn("public_profile,email", {
        success: function(user) {
            if (!user.existed()) {
                console.log('Listo')
                FB.api('/me?fields=id,name,email,permissions', function (response) {
                    user.set('username', response.name);
                    user.set('email', response.email);

                    user.save(null, {
                        success: function(user) {
                            alert('User logged in and sign up through Facebook, with username: ' + user.get('username') + ' and email: ' + user.get('email'));

                            // You should redirect the user to another page after a successful login.
                            window.location.replace('http://js-fb-login.back4app.io/logout.html');
                        },
                        error: function(user, error) {
                            alert('Failed to save user to database with error: ' + error.message);
                        }
                    });
                });
            } else {
                alert("User logged in through Facebook!");
                // You should redirect the user to another page after a successful login.
                window.location.replace('http://js-fb-login.back4app.io/logout.html');
                console.log('Ya está auth')
            }

            let authfacebook = document.querySelector('#authfacebook')
            authfacebook.classList.replace('fadeIn', 'fadeOut')
            let datospersonales = document.querySelector('#datospersonales')
            datospersonales.classList.replace('fadeOut', 'fadeOut')
        },
        error: function(user, error) {
            link();
        }
    });

    let authfacebook = document.querySelector('#authfacebook')
    authfacebook.classList.replace('fadeIn', 'fadeOut')
    let datospersonales = document.querySelector('#datospersonales')
    datospersonales.classList.replace('fadeOut', 'fadeIn')
}

function link() {
    var user = Parse.User.current();
    if (!Parse.FacebookUtils.isLinked(user)) {
        Parse.FacebookUtils.link(user, null, {
            success: function(user) {
                alert("Woohoo, user logged in with Facebook!");
            },
            error: function(user, error) {
                alert("User cancelled the Facebook login or did not fully authorize.");
            }
        });
    }
    else {
        alert("Can't link user to facebook because he is already linked");
    }
}

function selectProvincia(){
    const provincia = document.querySelector('#dpProvincia')
    
    var user = Parse.User.current()
    user.set('provincia', provincia.value)

    user.save().then((result) => {
        let datospersonales = document.querySelector('#datospersonales')
        datospersonales.classList.replace('fadeIn', 'fadeOut')
        let inicio = document.querySelector('#inicio')
        inicio.classList.replace('fadeOut', 'fadeIn')
    }).catch((err) => {
        console.log(`Error: ${err.message}`)
    });
}

function addMotoUser(status){
    User = Parse.User.current()
    User.set('conmoto', status)
    User.save().then((result)=>{
        if (!status){
            let tipoVE = document.querySelector("#tipoVE")
            let marcaVE = document.querySelector("#marcaVE")

            tipoVE.value = "moto"
            marcaVE.value = "pagary"

            tipoVE.disabled = true
            marcaVE.disabled = true
        }

        let inicio = document.querySelector('#inicio')
        inicio.classList.replace('fadeIn', 'fadeOut')
        let calcularForm = document.querySelector('#calcularForm')
        calcularForm.classList.replace('fadeOut', 'fadeIn')

        hadEbike = document.querySelector("#checkHadEbike")
        hadEbike.checked = status 
    }).catch((err)=>{
        console.log(`Error: ${err.message}`)
    })
}

var Datos = Parse.Object.extend("DatosConsumo");
