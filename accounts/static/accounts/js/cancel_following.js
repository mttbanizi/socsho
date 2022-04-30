$('.cancel_following').click(function(){
    
    console.log("clicked")
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
      
    var user_id = $(this).attr('data-id');
    $(this).attr({id:"active_follow"})
    var btn_text = "follow"
    
    var url = '/accounts/cancel_following/';
    var btn_class = 'btn btn-primary text-center mx-auto following_btn';
        
    console.log(user_id); 
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'user_id': user_id,
        },
        success: function(data){
           
            if(data['status'] == 'ok'){
                $("#active_follow").text(btn_text);
                $("#active_follow").attr({'class':btn_class});
                $("#active_follow").attr({'id':"following_btn"});

            }
            else {

            }
        }

    });
    

});