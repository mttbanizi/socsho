
      const sender = JSON.parse(document.getElementById('sender').textContent);

<<<<<<< HEAD

=======
>>>>>>> c6b8239e5fd427b81caa1cac9b31bb3855960e2f
      const chatSocket2 = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/dual_message/'
            + 'listener'
            + '/'
        );

        chatSocket2.onopen = function(e) {
            console.log('on Open unread_messages');
            chatSocket2.send(JSON.stringify({'command': 'unread_messages',  'username':sender}));
        }

      chatSocket2.onmessage = function(e) {
        
        var data = JSON.parse(e.data);
<<<<<<< HEAD
          console.log('notif data:'+data);
          if(data['reciever'] == sender){
            if(data['__str__'] != sender ){
                  console.log('notif : '+data['content']);
=======
          console.log(data);
          if(data['reciever'] == sender){
            if(data['__str__'] != sender ){
                  console.log('notif : '+data['content']);
                  
>>>>>>> c6b8239e5fd427b81caa1cac9b31bb3855960e2f
                  let divchat = document.getElementById('dropdown_chat_list');
                  let message_item = document.createElement("a");
                  let message_deail = document.createElement("div");
                  message_item.innerHTML=data['__str__'];
<<<<<<< HEAD
                  message_item.href="../single_message/dual_room_email/' " + data['__str__'] + " %}";
=======
                  message_item.href='/' + data['__str__'] + "/";
>>>>>>> c6b8239e5fd427b81caa1cac9b31bb3855960e2f
                  console.log(message_item.href);
                  message_item.className="message_item_class";
                  message_deail.className="message_detail_class";
                  message_deail.style.display='none';
                  message_deail.innerHTML=data['content'];
                  divchat.appendChild(message_item);
                  divchat.appendChild(message_deail);
                  
                  $(".message_item_class").hover(function(){
                    $(this).next().toggle();
                  });

                  if (!("Notification" in window)) {
                    alert("This browser does not support desktop notification");
                  }
            
                  // Let's check whether notification permissions have already been granted
                  else if (Notification.permission === "granted") {
                    // If it's okay let's create a notification
                    var notification = new Notification(data['__str__']+" : "+data['content']);
                  }
              
                  // Otherwise, we need to ask the user for permission
                  else if (Notification.permission !== "denied") {
                    Notification.requestPermission().then(function (permission) {
                      // If the user accepts, let's create a notification
                      if (permission === "granted") {
                        var notification = new Notification("Hi there!");
                      }
                    });
                  }
                  
              
            }
          }
      }
      