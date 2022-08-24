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
        

});


var map;  
var markers = [];
const LaPlata = {
    north: -34.81936536255149, //-34.81936536255149, -57.96880667574618
    south: -35.02991601497499, //-35.02991601497499, -57.950256047701615
    west: -58.14412828713677, //-34.95720890319979, -58.14412828713677
    east: -57.80657962260428, //-34.94260009885324, -57.80657962260428
  };

function initMap() {
    // create the maps
    var lat_lng = {lat: -34.921370606389594, lng: -57.95480962673844}; 

    map = new google.maps.Map(document.getElementById('map'), {  
        zoom: 15,
        center: lat_lng,
        restriction: {
            latLngBounds: LaPlata,
            strictBounds: false,
        } , 
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

  $(document).on('input', '.filter-table', function () {
    var tableName = $(this).attr('data-table-id');
    var searchKey1 = $("[data-column-id='1']").val().toLowerCase();
    var searchKey2 = $("[data-column-id='2']").val().toLowerCase();
    var searchKey5 = $("[data-column-id='5']").val();
    
    $("#" + tableName + " tbody tr").filter(function () {
      var columnSearch1 = !searchKey1 || $(this).children().eq(0).text().toLowerCase().indexOf(searchKey1) > -1;
      var columnSearch2 = !searchKey2 || $(this).children().eq(1).text().toLowerCase().indexOf(searchKey2) > -1;
      var columnSearch5 = !searchKey5 || $(this).children().eq(4).text().toLowerCase().indexOf(searchKey5) > -1;
      $(this).toggle(columnSearch1 && columnSearch2 && columnSearch5);
    }); 
  });
