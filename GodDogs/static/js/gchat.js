var interval = 4000; //4 seconds
function sendMessage() {
    $.ajax({
        url: "{{ url_for('receiveMessage') }}", 
        type: "POST", 
        data: {
        'chatText': $("#chatText").val(),
        },
        success: function() {
            recvMessage(),
            $("#chatText").val('');
        }
    });
}
function recvMessage() {
    $.ajax({
        url: "{{ url_for('sendMessagesList') }}",
        type: "GET",
        success: function(result) {
            $("#panelBody").html(result);            
        },
        complete: function(result) {
            setTimeout(recvMessage, interval);
        }
    });
}
$(document).ready(function() {
    $("#chatText").keypress(function(e) {
        if (e.keyCode == 13) {
            $("#send").click();
        }
    });
    $("button").click(sendMessage);
    setTimeout(recvMessage, interval);
});
