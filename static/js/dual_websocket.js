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
          console.log(data.content);

        }
        if (author === sender) {
          msgListTag.className = 'sent';
        } else {
          msgListTag.className = 'replies';
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