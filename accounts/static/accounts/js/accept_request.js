$('.accept_request').click(function(){
    
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
    $(this).attr({id:"active_request"})
    var btn_text = "accepted"
    
    var url = '/accounts/accept_request/';
    var btn_class = 'btn btn-primary text-center mx-auto';
        
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
                $("#active_request").text(btn_text);
                $("#active_request").attr({'class':btn_class});
                $("#active_request").attr({'id':"finnished"});

            }
            else {

            }
        }

    });
    

});