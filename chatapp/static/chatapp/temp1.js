$('#chat-form').on('submit', function (event) {
    event.preventDefault();

    $.ajax({

        url: '/post/',
        type: 'POST',
        data: { msgbox: $('#chat-msg').val() },

        success: function (json) {
            $('#chat-msg').val('');
            var val = Number(json.id);
            $('#msg-list').append('<li class="text-right list-group-item" value="' + val + '">' + json.msg + '</li>');
            console.log('<li class="text-right list-group-item" value="' + json.id + '">' + json.msg + '</li>');
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
});


function getMessages() {
    url = '/messages?id=' + chatlastid;
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var messages = req.responseText;
            console.log(messages);
            $('#msg-list').append(messages);
            var lastli = document.getElementsByTagName('li');
            var val = lastli[lastli.length - 1].value;
            val = Number(val);
            chatlastid = val;
        }
    };

    req.open("GET", url, true);
    req.send();

    console.log(chatlist.scrollHeight - chatlist.offsetHeight - chatlist.scrollTop)

    if ((chatlist.scrollHeight - chatlist.offsetHeight - chatlist.scrollTop) < 200) {
        chatlist.scrollTop = chatlist.scrollHeight
    } 
}

$(function () {
    refreshTimer = setInterval(getMessages, 500);
});

$(document).ready(function () {
    $('#send').attr('disabled', 'disabled');
    $('#chat-msg').keyup(function () {
        if ($(this).val() != '') {
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
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});