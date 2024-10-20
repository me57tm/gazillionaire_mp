 $(document).ready(function() {

    var socket = io();

    socket.on('update_title', function(msg, cb) {
        console.log("Got data: " + msg);
        $("#title-text").text(msg["title"]);
        $("#title-image").attr("src","/static/title_images/"+msg["image"]);
    });
});