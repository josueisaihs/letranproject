$(document).ready(function(){
    $(`#id_subject option[value=${subject}]`)[0].selected = true;

    actualizarDatos();

    try {
        var toastError = new bootstrap.Toast(document.getElementById("id_toastError"), 'autohide');
    } catch (error) {
        
    }

    $("#inputGroupFile01").change(function(){
        let curfiles = $("#inputGroupFile01")[0].files;
        if (curfiles.length === 0){
            $(".file-name").html("No ha seleccionado");
        }else if (validateFileSize(curfiles[0].size)){
            const typeFile = detectarFileType(curfiles[0].name);
            if (typeFile){
                $(".form-file").addClass("invisible");
                $(".form-upload").removeClass("invisible");
                $(".form-upload .text").html(`Subiendo "${curfiles[0].name}" de ${returnFileSize(curfiles[0].size)}`);
                $(".file-name").html(`${curfiles[0].name} ${returnFileSize(curfiles[0].size)}`);
                let fd = new FormData();
                fd.append('recurso', curfiles[0]);
                fd.append('name', curfiles[0].name)
                fd.append('tipo', typeFile.tipo)
                fd.append('courses', 1)
                $.ajax({
                    type: "POST",
                    url: urlupload,
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        $(".form-file").removeClass("invisible");
                        $(".form-upload").addClass("invisible");

                        if (response.response){
                            $(".file-name").html("Archivo...");
                            let atag = `<a class="d-inline-flex border px-2 rounded m-1" role="button" data-name="${curfiles[0].name}" onclick="$(this).remove();removeFile('${curfiles[0].name}', ${curfiles[0].size});">
                                <div class="d-flex flex-column text-center text-small py-1">
                                    <div class="text-primary">
                                        <i class="${typeFile.icon}"></i> ${curfiles[0].name}
                                    </div>
                                </div>
                                <div class="ml-2 flex-fill align-self-center text-small">
                                    ${returnFileSize(curfiles[0].size)}
                                </div>
                                <div class="ml-2 flex-fill align-self-center text-small">
                                    <i class="fas fa-times"></i>
                                </div>
                            </a>`
                            $(".files-upload").append(atag);
                            
                            filesUpload += 1;
                            filesSize += curfiles[0].size;
                            
                            
                            if (recursos.name.indexOf(curfiles[0].name) < 0)
                                recursos.name.push(curfiles[0].name)
                            
                            actualizarDatos();
                        }else{
                            $(".file-name").html(`No se pudo subir "${curfiles[0].name}"`);

                            $(".toast-error-text").html(`No se pudo subir "${curfiles[0].name}"`);
                            toastError.show();
                        }
                    },
                    error: (xhr, errmsg, err)=>{
                        $(".form-file").removeClass("invisible");
                        $(".form-upload").addClass("invisible");

                        $(".toast-error-text").html(`${err}. :( No se pudo subir "${curfiles[0].name}"`);
                        toastError.show();
                    }
                });
            }else{
                $(".toast-error-text").html(`El archivo "${curfiles[0].name}" no tiene un formato permitido.`);
                toastError.show();
            }
        }else{
            $(".toast-error-text").html(`El archivo "${curfiles[0].name}" con ${returnFileSize(curfiles[0].size)}, supera con ${validateFileSize(curfiles[0].size, true)} los 250MB permitidos.`);
            toastError.show();
        }
    });

    $("#id_salvar").on('click', (e)=>{
        e.preventDefault();
        const data = window.editors[0].getData();
        $("#id_classbody").html(data);

        $("#id_classform").submit();
    });
});

function returnFileSize(number) {
    if(number < 1024) {
      return (number + ' bytes').replace('.', ',');
    } else if(number >= 1024 && number < 1048576) {
      return ((number/1024).toFixed(1) + ' KB').replace('.', ',');
    } else if(number >= 1048576) {
      return ((number/1048576).toFixed(1) + ' MB').replace('.', ',');
    }
}

function validateFileSize(number, dif=false){    
    // Hasta 250 MB
    const MAXSIZE = 262144000
    if (dif)
        return returnFileSize(number - MAXSIZE)
    else
        return number <= MAXSIZE
}

function detectarFileType(filePath){
    const imageExtensions = /(.jpg|.jpeg|.png)$/i;
    const videoExtensions = /(.mp4|.mpg|.ogg)$/i;
    const documentExtensions = /(.doc|.docx|.pdf|.ppt|.pttx)$/i;
    const audioExtensions = /(.mp3|.wav)$/i;
    const htmlExtensions = /(.html)$/i;
    const cssExtensions = /(.css|.sass|.scss)$/i;
    const jsExtensions = /(.js|.ts)$/i;
    const pythonExtensions = /(.py|.pyc)$/i;    

    if (imageExtensions.exec(filePath))
        return {tipo: "image", icon: "fa fa-file-image"} 
    else if (videoExtensions.exec(filePath))
        return {tipo: "video", icon: "fa fa-file-video"}
    else if (documentExtensions.exec(filePath))
        return {tipo: "documento", icon: "fa fa-file-alt"}
    else if (audioExtensions.exec(filePath))
        return {tipo: "audio", icon: "fa fa-file-audio"}
    else if (htmlExtensions.exec(filePath))
        return {tipo: "html", icon: "fa fa-file-code"}
    else if (cssExtensions.exec(filePath))
        return {tipo: "css", icon: "fa fa-file-code"}
    else if (jsExtensions.exec(filePath))
        return {tipo: "js", icon: "fa fa-file-code"}
    else if (pythonExtensions.exec(filePath))
        return {tipo: "python", icon: "fa fa-file-code"}
    else
        return false
}

function actualizarDatos(){    
    if (filesUpload > 0){
        $(".badge-files").removeClass("invisible");
        $(".badge-files").html(filesUpload);
    }else{
        $(".badge-files").addClass("invisible");
    }
    
    if (filesSize > 0){
        $(".files-size").removeClass("invisible")
        $(".files-size").html(returnFileSize(filesSize));
    }else{
        $(".files-size").addClass("invisible")
    }

    $("#id_recursosjson").val(JSON.stringify(recursos)) 
}

function removeFile(name, fileSize){
    filesUpload -= 1;
    filesSize -= fileSize;
    recursos.name = recursos.name.filter((value, index, arr)=>{return value !== name})
    actualizarDatos();
}

function removeClass(slug){
    $.ajax({
        type: "post",
        url: urldeleteclass,
        data: {"slug": slug},
        success: function (response) {
            if (response.response){
                window.location = urlindex;
            }
        },
        error: (xhr, errmsg, err)=>{
            console.log(err, errmsg);
        }
    });
}
