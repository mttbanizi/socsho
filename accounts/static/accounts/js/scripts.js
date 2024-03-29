$('#following_btn').click(function(){
    

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
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
    
   
    
    
    var user_id = $('#following_btn').attr('data-id');
    var follow = $('#following_btn').text();
    
    if(follow == 'follow'){
        var url = '/accounts/follow/'
        var btn_text = 'unfollow'
        var btn_class = 'btn btn-warning text-center mx-auto'
    }else{
        var url = '/accounts/unfollow/'
        var btn_text = 'follow'
        var btn_class = 'btn btn-primary text-center mx-auto'
    }
    
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'user_id': user_id,
        },
        success: function(data){
            if(data['status'] == 'private'){
                $('#following_btn').text("follow requested");
                $('#following_btn').attr({'class':btn_class});
            }
            if(data['status'] == 'ok'){
                $('#following_btn').text(btn_text);
                $('#following_btn').attr({'class':btn_class});
            }
        }

    });
    

});