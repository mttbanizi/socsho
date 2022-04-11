
      const sender = JSON.parse(document.getElementById('sender').textContent);

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
          console.log(data);
          if(data['reciever'] == sender){
            if(data['__str__'] != sender ){
                  console.log('notif : '+data['content']);
                  let divchat = document.getElementById('dropdown_chat_list');
                  let message_item = document.createElement("a");
                  let message_deail = document.createElement("div");
                  message_item.innerHTML=data['__str__'];
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
          if (data['command'] === 'unread_messages') {
            for (let i=data['content'].length-1; i>=0 ; i--) {
              append_messages(data['content'][i]);
          }
        } 
      }

      function append_messages(data){
        let divchat = document.getElementById('dropdown_chat_list');
        let message_item = document.createElement("a");
        let finder=":contains("+data['__str__']+")";
        message_item.className="message_item_class";
        console.log(data['__str__']);
        if ($(".message_item_class").length){
          $(".message_item_class").each(function () {
            var exist_email=$(this).children(":first").text();
            console.log(data['content']);
            console.log(exist_email);
            if(data['__str__']  ==exist_email ){
              var message_deail= $("<p class='message_detail_class'></p>").text(data['content']);
              console.log($(message_deail));
              $(this).append(message_deail);
              $(message_deail).hide();
              $(".message_item_class").hover(function(){
                $(this).children('.message_detail_class').toggle();
              });
            }
          });
        }
        else {
          let message_item = document.createElement("a");
          let message_deail = document.createElement("p");
          message_item.innerHTML="<span>"+data['__str__']+"</span>";
          console.log(message_item.href);
          message_item.className="message_item_class";
          message_deail.className="message_detail_class";
          message_deail.style.display='none';
          message_deail.innerHTML=data['content'];
          divchat.appendChild(message_item);
          message_item.appendChild(message_deail);
          
        }
        
        
      }

      

      const reciever = JSON.parse(document.getElementById('reciever').textContent);
      const roomName = JSON.parse(document.getElementById('roomname').textContent);
      

      const chatSocket_dual = new WebSocket(
          'ws://'
          + window.location.host
          + '/ws/dual_message/'
          + roomName
          + '/'
      );

     
    
    chatSocket_dual.onopen = function(e) {
        console.log('on Open');
        chatSocket_dual.send(JSON.stringify({'command': 'fetch_message', 'roomname': roomName, 'username':sender}));
    }

      chatSocket_dual.onmessage = function(e) {
          const data = JSON.parse(e.data);
       //   document.querySelector('#chat-log').value += (data.message + '\n');
          console.log('on_messgae');
        
        console.log(data);
        if (data['command'] === 'fetch_message') {
            for (let i=data['content'].length-1; i>=0 ; i--) {
            createMessage(data['content'][i]);
          }
        }

        else if (data['command'] === "new_message" ){
          createMessage(data);
          }

        else if(data['command'] === 'img'){

          createMessage(data);


        }
      }; 

      function createMessage(data) {
      var author = data["__str__"];
      var command = data['command'];

      if(command == "img"){

        var msgListTag = document.createElement('li');
        var imgTag = document.createElement('img');
        imgTag.src = data['content'];
        msgListTag.appendChild(imgTag);
      }

      else{
        
        var msgListTag = document.createElement('li');
        var pTag = document.createElement('p');
        pTag.textContent = data.content;
        msgListTag.appendChild(pTag);
        console.log('content');
        console.log(data);

      }
      if (author === sender) {
        msgListTag.className = 'sent';
      } else {
        msgListTag.className = 'replies';
        if (command =="new_message"){
          data = {"command":"set_read", "sender": author, "reciever": sender, "room_name": data['room_name']};
          chatSocket2.send(JSON.stringify(data));
        }
        
      }
      console.log('append');
      document.querySelector('#chat-log').appendChild(msgListTag);
      
    } 
    

    document.querySelector('#chat-message-submit').onclick = function(e) {
          const messageInputDom = document.querySelector('#chat-message-input');
          const message = messageInputDom.value;
          
          chatSocket_dual.send(JSON.stringify({
              'message': message,
              'command': 'new_message',
              'sender' : sender,
              'reciever':reciever,
              'roomname': roomName,
              'username':sender
          }));
          messageInputDom.value = '';
    };   