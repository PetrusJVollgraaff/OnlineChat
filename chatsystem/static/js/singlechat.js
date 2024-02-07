class ChatBubble{
    constructor(data){
        this.username   = data.username,
        this.message    = data.message
    }

    build(){
        return '<div class="text_bubble">'+this.username + ': ' + this.message + '</div>'
    }
}

class ChatBubbles{
    constructor(data){
        this.messages = data
    }

    buildBubble(data){
        var bubble = new ChatBubble(data)
        document.getElementById('#chat-text').insertAdjacentHTML("beforeend", bubble.build() )
    }

    build(){
        var _ = this;
        this.messages.forEach(function(item, index){
            _.buildBubble(item)
        })
    }

    eventlistners(){
        var _ = this;

        document.querySelector('#chat_form').onsubmit = function (e) {
            const messageInputDom = document.querySelector('#input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({ 'message': message }));
            
            messageInputDom.value = '';
        
            return false;
        };
        
        
        chatSocket.onmessage = function (e) {
            _.buildBubble( JSON.parse(e.data) );
        }
    }
}

(function () {
    
    fetch('/getBubbles', {
        method: "GET",
        headers: { "X-CSRFToken": getCookie("csrftoken"), }
    })
    .then((response) => {return response.json()})
    .then((data) => { 
        console.log(data)
        var bubbls = new ChatBubbles(data)
        bubbls.build()
        bubbls.eventlistners()
    })
        
})();