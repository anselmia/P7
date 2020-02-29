$(function () {
    function initializeMap(geometry, id) {

        var myLatLng = geometry.location;

        var map = new google.maps.Map(id, {
            zoom: 15,
            center: myLatLng
        });

        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            animation: google.maps.Animation.DROP
        });

        function toggleBounce() {
            if (marker.getAnimation() !== null) {
                marker.setAnimation(null);
            } else {
                marker.setAnimation(google.maps.Animation.BOUNCE);
            }
        }

        var ne_lat = geometry.viewport.northeast.lat;
        var ne_lng = geometry.viewport.northeast.lng;
        var sw_lat = geometry.viewport.southwest.lat;
        var sw_lng = geometry.viewport.southwest.lng;

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

    var $msg_card_body, EntryForm;
    $msg_card_body = $('#msg_card_body');
    EntryForm = $('#EntryForm');
    $("#grandpy_writing").hide();
    EntryForm.on('submit', function (e) {
        e.preventDefault();
        var text = $.trim($('#text').val());
        text = text.split('<').join('&lt;');
        text = text.split('>').join('&gt;');
        if (text.trim()) {
            $msg_card_body.append('<div class="d-flex justify-content-end mb-4' +
                ' main_user_img" id="user_msg_template">' +
                '<div class="msg_cotainer_send">' +
                '<p class="small">' + text + '</p>' +
                '</div>' +
                '<div class="img_cont_msg">' +
                '<img src="../static/images/baby.png"' +
                ' class="rounded-circle user_img_msg">' +
                '</div>' +
                '</div>');
            $.trim($('#text').val(''));
            $("#msg_card_body").stop().animate({ scrollTop: $("#msg_card_body")[0].scrollHeight }, 1000);
            $.post('/_response', { text: text }).done(function (answer) {
                $("#grandpy_writing").show();
                setTimeout(function () {
                    $msg_card_body.append('<div class="d-flex justify-content-start mb-4" id="grandpy_msg_template">' +
                        '<div class="img_cont_msg">' +
                        '<img src="../static/images/grandfather.png" class="rounded-circle user_img_msg"></div>' +
                        '<div class="msg_cotainer">' +
                        '<p class="small">' + answer['answer'] + '</p>' +
                        '</div>' +
                        '</div>');
                    if (answer['wiki_answer']) {
                        $msg_card_body.append('<div class="d-flex justify-content-start mb-4" id="grandpy_msg_template">' +
                            '<div class="img_cont_msg">' +
                            '<img src="../static/images/grandfather.png" class="rounded-circle user_img_msg"></div>' +
                            '<div class="msg_cotainer">' +
                            '<p class="small">' + answer['wiki_answer'] + '</p>' +
                            '</div>' +
                            '</div>');
                    }
                    if (answer['geometry']) {
                        if (document.contains(document.getElementById("mapid"))) {
                            var element = document.getElementById("mapid");
                            element.parentNode.removeChild(element);
                        }
                        $msg_card_body.append('<div class="d-flex justify-content-start mb-4"' +
                            ' id="grandpy_msg_template">' +
                            '<div class="img_cont_msg">' +
                            '<img src="../static/images/grandfather.png" class="rounded-circle user_img_msg"></div>' +
                            '<div class="msg_cotainer" id="mapidbox">' +
                            '<div id="mapid">' +
                            '</div>' +
                            '</div>' +
                            '</div>');
                        $("<div></div>").hide().appendTo($("#mapid")).fadeIn('slow', function () {

                            initializeMap(answer['geometry'],
                                document.getElementById("mapid"));

                        });
                    }
                    $("#grandpy_writing").hide();
                    playSound()
                    $("#msg_card_body").stop().animate({ scrollTop: $("#msg_card_body")[0].scrollHeight }, 1000);
                }, 3000);
            })
        }
    });
});

function playSound() {
    var sound = document.getElementById("audio");
    sound.play();
};
