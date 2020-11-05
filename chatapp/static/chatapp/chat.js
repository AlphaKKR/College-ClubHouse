var send = true;
$('#chat-form').on('submit', function(event) {
    event.preventDefault();
   if (send==true){
    send=false;
    $.ajax({
        url: '../post',
        type: 'POST',
        data: { msgbox: $('#chat-msg').val().trim(), room_data: roomid},

        success: function(json) {
            $('#chat-msg').val('');
            var val = Number(json.id);
            $('#msg-list').append('<li class="text-right list-group-item" value="'+ val +'">' + json.msg + '</li>');
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
            send=true;
        }
    });
}
});




 function getMessages(){
     
    url='../messages?id='+ chatlastid + '&room_id=' + roomid;
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
            var messages = req.responseText;
            $('#msg-list').append(messages);
            var lastli = document.getElementsByTagName('li');
            var val = lastli[lastli.length-1].value;
            val = Number(val);
            chatlastid = val;
      }
    };
    
    req.open("GET",url, true);
    req.send();
    if (refresh){
        var chatlist = document.getElementById('msg-list-div');
        chatlist.scrollTop = chatlist.scrollHeight;

    }
}


var refresh = true;
$(function() {
    $('#msg-list-div').on('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight-20) {
            refresh=true;
        }
        else{
            refresh=false;
        }
    });
    

    refreshTimer = setInterval(getMessages, 500);
});

$(document).ready(function() {
    $('#send').attr('disabled', 'disabled');
    $('#chat-msg').keyup(function() {
        if ($('#chat-msg').val()[0]==' '){
            $('#chat-msg').val('');
        }
        if ($('#chat-msg').val() != '') {
            $('#send').removeAttr('disabled');
        } else {
            $('#send').attr('disabled', 'disabled');
        }
    });
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});