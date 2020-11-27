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

    var inciWebData = new google.maps.KmlLayer({ url: 'https://inciweb.nwcg.gov/feeds/maps/' });
    inciWebData.setMap(map);

    var bounds = new google.maps.LatLngBounds();

    $.each(customers, function(i, e) {
        var long = Number(e['longitude']);
        var lat = Number(e['latitude']);
        var latlng = new google.maps.LatLng(lat, long);

        bounds.extend(latlng);

        // Create the marker
        new google.maps.Marker({ // Set the marker
            position : latlng, // Position marker to coordinates
            map : map, // assign the market to our map variable
            //customInfo: contentStr,
            //icon: icons[e['report_type']]
        });
    });
    map.fitBounds(bounds);
}


function getCustomerData(latest=false) {
    $.ajax({
        url: '/mapCustomers',
        success: function(customers) {
            console.log(customers);
            // Lab 6: Question 4: Bonus - center map over newly submitted report
            // if (latest) {
            //     // Get latest report
            //     let lastReport = reports.reduce(function (prev, curr) {
            //         return (prev.time_stamp > curr.time_stamp) ? prev : curr
            //     });
            //     reports = [];
            //     reports.push(lastReport);
            //     console.log(reports);
            // }
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