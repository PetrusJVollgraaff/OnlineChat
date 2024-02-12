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
        this.messages       = data
        this.nestedElement  = document.getElementById('#chat-text')
    }

    buildBubble(data){
        var bubble = new ChatBubble(data)
        this.nestedElement.insertAdjacentHTML("beforeend", bubble.build() )
    }

    build(){
        var _ = this;
        this.messages.forEach(function(item, index){
            _.buildBubble(item)
        })
        _.nestedElement.scrollTo(0, _.nestedElement.scrollHeight);
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
            _.nestedElement.scrollTo(0, _.nestedElement.scrollHeight);
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
        var bubbls = new ChatBubbles(data)
        bubbls.build()
        bubbls.eventlistners()

        var videoelm = new VideoSystem()

        videoelm.eventlistner()
    })
        
})();