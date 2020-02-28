
var wait = $('#wait');
var map = $('#map');
var submit = $('#submit');
var user_message = $('#user_message');
 
wait.hide();
var maps_api_url = "https://maps.googleapis.com/maps/api/js?key=" + $GMAPS_KEY;

$.getScript(maps_api_url, function () {
    //using getscript to ensure gmaps api is loaded
    function initializeMap(name, json, id) {

        var myLatLng = json.candidates[0].geometry.location;

        var map = new google.maps.Map(id, {
            zoom: 15,
            center: myLatLng
        });

        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: name,
            animation: google.maps.Animation.DROP
        });

        function toggleBounce() {
            if (marker.getAnimation() !== null) {
                marker.setAnimation(null);
            } else {
                marker.setAnimation(google.maps.Animation.BOUNCE);
            }
        }

        var ne_lat = json.candidates[0].geometry.viewport.northeast.lat;
        var ne_lng = json.candidates[0].geometry.viewport.northeast.lng;
        var sw_lat = json.candidates[0].geometry.viewport.southwest.lat;
        var sw_lng = json.candidates[0].geometry.viewport.southwest.lng;

        var ne_bound = new google.maps.LatLng(ne_lat, ne_lng);
        var sw_bound = new google.maps.LatLng(sw_lat, sw_lng);
        var bounds = new google.maps.LatLngBounds();

        bounds.extend(ne_bound);
        bounds.extend(sw_bound);

        map.fitBounds(bounds);

        setTimeout(function () {
            marker.setMap(map);
            toggleBounce();
        }, 3000);

    }

    submit.on('click', function (e) {
        //function to handle form submission
        e.preventDefault();

        if (user_message.val()) {
            $.ajax({
                url: $SCRIPT_ROOT + '/_response',
                type: 'POST',
                data: {user_message : user_message.val()},

                success: function (response, status) {

                    // Ajax call successful : handle the response.
                    var input = $("<div>").text(user_message.val()).html();
                    user_message.val("");

                    if (input !== "") { //second check of input content in case of multiple sending of the message
                       
                        //Display wait message for 1.2 secs, then display response
                        wait.delay(200).fadeIn(1200).fadeOut('slow', function () {

                            if (response['gmaps_reply'] !== "No result") {

                                $("<div id='" + map + "'></div>").hide().appendTo(map).fadeIn('slow', function () {

                                        initializeMap(response['gmaps_name'],
                                            response['gmaps_json'],
                                            document.getElementById(map));
                                    });

                            }
                            else {
                               
                            }

                            //$("<div class='row'><div class='message bot'>" + response['wiki_reply'] + "</div></div>").hide().appendTo(chat_msg).show('slow');
                        });
                    }
                },

                error: function (response, status, error) {
                    alert("There was a problem with the ajax request: " + error);

                },

                complete: function () {
                }
            });
        }
    });
});
