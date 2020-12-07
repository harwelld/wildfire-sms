var map;
var place;
var autocomplete;
var infowindow = new google.maps.InfoWindow();


const icons = {
    miles5: {
        name: '5 miles',
        url: 'static/img/crimson.svg',
        scaledSize: new google.maps.Size(35, 35)
    },
    miles10: {
        name: '10 miles',
        url: 'static/img/orange.svg',
        scaledSize: new google.maps.Size(35, 35)
    },
    miles15: {
        name: '15 miles',
        url: 'static/img/green.svg',
        scaledSize: new google.maps.Size(35, 35)
    },
    miles20: {
        name: '20 miles',
        url: 'static/img/blue.svg',
        scaledSize: new google.maps.Size(35, 35)
    }
};

function setMapIcon(user_distance) {
    let icon;
    if (user_distance === 5) {
        icon = icons['miles5'];
    } else if (user_distance === 10) {
        icon = icons['miles10'];
    } else if (user_distance === 15) {
        icon = icons['miles15'];
    } else {
        icon = icons['miles20'];
    }
    return icon;
}


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

    // Create custom ledgend for user locations
    const legend = document.getElementById('legend');
    for (const key in icons) {
        const type = icons[key];
        const name = type.name;
        const icon = type.url;
        const p = document.createElement('p');
        p.innerHTML = '<img class="ml-3" src="' + icon + '"> ' + name;
        legend.appendChild(p);
    }
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(legend);

    // Load latest InciWeb data direct from RSS feed
    var inciWebData = new google.maps.KmlLayer({ url: 'https://inciweb.nwcg.gov/feeds/maps/' });
    inciWebData.setMap(map);

    // This fails because of CORS
    // map.data.loadGeoJson('https://inciweb.nwcg.gov/feeds/json/esri/');
    // map.data.setStyle({
    //     url: 'static/img/error.svg',
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
            icon: setMapIcon(e['user_distance'])
        });

        // Add a Click Listener to the marker
        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(marker['customInfo']);
            infowindow.open(map, marker);
        });
    });
    map.fitBounds(bounds);
}


// Hit mapCustomer endpoint to retrieve customer data
function getCustomerData() {
    $.ajax({
        url: '/getCustomers',
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
    const autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete')
    );

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


// Initialize when page loads
google.maps.event.addDomListener(window, 'load', initialization);
