$(document).ready(function(){  

    $("#covid1S").click(function() {  
        document.getElementById('fechaC1').removeAttribute('hidden')
        document.getElementById('fechaC1Input').setAttribute('required', 'true')
        document.getElementById('divCovid2').removeAttribute('hidden')   
        document.getElementById('covid2S').setAttribute('required', 'true')
    });

    $("#covid1N").click(function() {  
        document.getElementById('fechaC1').setAttribute('hidden', 'true')
        document.getElementById('fechaC1Input').removeAttribute('required')
        document.getElementById('divCovid2').setAttribute('hidden', 'true ')  
        document.getElementById('covid2S').removeAttribute('required') 
    });  

    $("#covid2S").click(function() {  
        document.getElementById('fechaC2').removeAttribute('hidden')
        document.getElementById('fechaC2Input').setAttribute('required', 'true')
    }); 

    $("#covid2N").click(function() {  
        document.getElementById('fechaC2').setAttribute('hidden', 'true')
        document.getElementById('fechaC2Input').removeAttribute('required')
    });

    $("#gripeS").click(function() {  
        document.getElementById('fechaG').removeAttribute('hidden')
        document.getElementById('fechaGInput').setAttribute('required', 'true')
    });

    $("#gripeN").click(function() {  
        document.getElementById('fechaG').setAttribute('hidden', 'true')
        document.getElementById('fechaGInput').removeAttribute('required')
    });

    $("#fiebreAmarillaS").click(function() {  
        document.getElementById('fechaFB').removeAttribute('hidden')
        document.getElementById('fechaFBinput').setAttribute('required', 'true')
    });
    
    $("#fiebreAmarillaN").click(function() {  
        document.getElementById('fechaFB').setAttribute('hidden', 'true')
        document.getElementById('fechaFBinput').removeAttribute('required')
    })
    $("#fiebreAmarillaN").click(function() {  
        document.getElementById('fechaFB').setAttribute('hidden', 'true')
        document.getElementById('fechaFBinput').removeAttribute('required')
    })
    $("#recuperar_datos_ASTU").click(function() {  
        document.getElementById('row_nombre_apellido_ASTU').removeAttribute('hidden')
        document.getElementById('row_vacuna_ASTU').removeAttribute('hidden')
        document.getElementById('row_horario_ASTU').removeAttribute('hidden')
    })
        
    ;
});