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

var map;  
var markers = [];

function initMap() {
    // create the maps
    var lat_lng = {lat: -34.921370606389594, lng: -57.95480962673844}; 

    map = new google.maps.Map(document.getElementById('map'), {  
        zoom: 15,  
        center: lat_lng,  
        mapTypeId: google.maps.MapTypeId.TERRAIN  
    });

    map.addListener('click', function(event) {  
        addMarker(event.latLng);
    });  
}

function addMarker(location) {
    deleteMarkers()
    var marker = new google.maps.Marker({  
      position: location,  
      map: map  
    });
    document.getElementById('lat').value = location.lat()
    document.getElementById('lon').value = location.lng()
    markers.push(marker); 
}

function deleteMarkers(){
    hideMarkers();
    markers = [];
  }

function hideMarkers(){
    setMapOnAll(null);
}

function setMapOnAll(map) {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }
