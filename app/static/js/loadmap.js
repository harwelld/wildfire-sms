var map;
var place;
var autocomplete;
var infowindow = new google.maps.InfoWindow();


function initialization() {
    getCustomerData();
    initAutocomplete();
}


function mapInitialization(customers) {
    map = new google.maps.Map(document.getElementById('map'), {
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.TOP_CENTER,
        },
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.RIGHT_TOP,
        },
        fullscreenControl: true,
        scaleControl: true,
        streetViewControl: false
    });

    // Load latest InciWeb data direct from RSS feed
    var inciWebData = new google.maps.KmlLayer({ url: 'https://inciweb.nwcg.gov/feeds/maps/' });
    inciWebData.setMap(map);

    // This fails because of CORS - InciWeb must have this disabled
    // map.data.loadGeoJson('https://inciweb.nwcg.gov/feeds/json/esri/');
    // map.data.setStyle({
    //     url: 'img/error.svg',
    //     scaledSize: new google.maps.Size(40, 40)
    // });

    var bounds = new google.maps.LatLngBounds();

    $.each(customers, function(i, e) {
        console.log(e);
        var long = Number(e['longitude']);
        var lat = Number(e['latitude']);
        var latlng = new google.maps.LatLng(lat, long);

        bounds.extend(latlng);

        let contentStr = '<h4>User Location</h4><hr>';
        contentStr += '<p><b>' + 'Username' + ':</b>&nbsp' + e['user_name'] + '</p>';
        contentStr += '<p><b>' + 'Phone Number' + ':</b>&nbsp' + e['userphone'] + '</p>';
        contentStr += '<p><b>' + 'Notification Distance' + ':</b>&nbsp' + e['user_distance'] + ' miles</p>';

        // Create the marker
        let marker = new google.maps.Marker({ // Set the marker
            position : latlng, // Position marker to coordinates
            map : map, // assign the market to our map variable
            customInfo: contentStr,
            //icon: icons[e['report_type']]
        });

        // Add a Click Listener to the marker
        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(marker['customInfo']);
            infowindow.open(map, marker);
        });
    });
    map.fitBounds(bounds);
}


function getCustomerData() {
    $.ajax({
        url: '/mapCustomers',
        success: function(customers) {
            mapInitialization(customers);
        },
        error: function(status, error) {
            alert("An AJAX error occured: " + status + "\nError: " + error);
        }
    });
}


// Center map from autocomplete address field selection
function initAutocomplete() {
    const autocomplete = new google.maps.places.Autocomplete(document
        .getElementById('autocomplete'));

    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }
        // If the place has a geometry, then present it on the map
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        // Pass lat/lon values to hidden fields
        $('#latitude').val(place.geometry.location.lat());
        $('#longitude').val(place.geometry.location.lng());
    });
}

//Execute our 'initialization' function once the page has loaded.
google.maps.event.addDomListener(window, 'load', initialization);