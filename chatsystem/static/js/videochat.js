class VideoPopup{
    constructor(data){
        this.position   = data.position,
        this.title      = data.title,
        this.message    = data.message
        this.buttons    = data.buttons
        console.log(this)
    }

    close(){
        var elmP    = document.querySelector(".pop_call_notify")
        elmP.remove();
    }

    build(){
        document.querySelector('body').insertAdjacentHTML("beforeend",'<div class="pop_call_notify" data-pos="'+this.position+'"><div class="incomingWrapper">'+
                '<div class="itemWrapper"><h2>'+this.title+'</h2></div>'+
                '<div class="itemWrapper">'+this.message+'</div>'+
                '<div class="itemWrapper button_btn"></div></div></div>')

        this.buildbuttons()
    }

    buildbuttons(){
        var elmP    = document.querySelector(".pop_call_notify")
        var elmBtn  = elmP.querySelector(".itemWrapper.button_btn")
        this.buttons.forEach(function(btn, index){
            elmBtn.insertAdjacentHTML("beforeend",'<button class="actionButton">'+btn.title+'</button>')

            if(typeof btn.onclick != "undefined"){
                elmBtn.lastChild.addEventListener("click", function(){
                    btn.onclick(elmP)
                })
            }
        })
    }
}

class VideoSystem{
    constructor(){
        this.peerConnection = undefined
        this.localStream    = undefined
        this.remoteStream   = undefined
        this.isCaller = false
        this.servers = {
            iceServers:[
                {
                    urls:['stun:stun1.1.goolge.com:19302','stun:stun2.1.goolge.com:19302']
                }
            ]
        }
    }

    async #build(){
        var videoelm =  '<div id="videos">'+
                        '<video class="video-player" id="user-1" autoplay playsinline ></video>'+
                        '<video class="video-player" id="user-2" autoplay playsinline ></video>'+
                        '<div class="btn_ctn">'+
                        '<button id="End_Btn">End Call</button>'
                        '</div></div>'

        document.querySelector(".main_ctn[data-t='chat']").setAttribute('data-t', 'both')
        document.getElementById("video_ctn").insertAdjacentHTML("beforeend",  videoelm)

        //await this.#assignElm()
        //this.#extraEvents()

        await this.#getStreamVar()
    }

    eventlistner(){
        var _ = this;

        document.querySelector("#Call_Btn").addEventListener("click", function(){
            this.style.display = "none"
            _.isCaller = true
            _.#build()
            _.#extraEvents()
        })

        videoSocket.onmessage = function (event) {
            console.log(event)
            const data = JSON.parse(event.data);
            
            if(data.type == 'connection') {
                console.log(data.message)
            }
    
            if(data.type == 'call_received') {
                _.#buildNotifier()
            }

            if(data.type == 'call_ignored' || data.type == 'call_ended') {
                if (typeof popupMessage != "undefined"){
                    popupMessage.close()
                    popupMessage = undefined;
                }
                _.#StopCall()
            }
    
            if(data.type == 'call_answered') {
                console.log(data);
            }
            
            /*if (data.message.type === 'offer') {
                // Received SDP offer from the other peer
                _.#handleSDPOffer(data.message);
            } else if (data.message.type === 'answer') {
                // Received SDP answer from the other peer
                _.#handleSDPAnswer(data.message);
            } else if (data.message.type === 'ice-candidate') {
                // Received ICE candidate from the other peer
                _.#AddICECandidate(data.message);
            }*/
        };
    }

    async #getStreamVar(){
        var _ = this;

        //this.#build()
        await this.#setupLocalMedia().then(() => {
            _.#createPeerConnection();
            _.#createOffer();
        });
    }

    async #setupLocalMedia(){
        try {
            this.localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:false})
            document.getElementById("user-1").srcObject = this.localStream;
        } catch (error) {
            console.error('Error accessing local media:', error);
        }
    }

    #extraEvents(){
        var _ = this
        console.log("world")
        document.querySelector("#End_Btn").addEventListener("click", function(){
            videoSocket.send(JSON.stringify({type: 'call_end'})); 
            _.localStream = undefined
        })
    }

    #StopCall(){
        document.querySelector(".main_ctn[data-t='both']").setAttribute('data-t', 'chat')
        document.getElementById("video_ctn").innerHTML = ""
        document.querySelector("#Call_Btn").style.display = ""
    }


    #createPeerConnection() {
        var _ = this
        this.peerConnection = new RTCPeerConnection(_.servers);
    
        // Add local stream to peer connection
        _.localStream.getTracks().forEach(track => _.peerConnection.addTrack(track, _.localStream));
    }

    async #createOffer() {
          const offer = await this.peerConnection.createOffer();
          await this.peerConnection.setLocalDescription(offer);
          videoSocket.send(JSON.stringify({type: 'call', rtcMessage: offer}));
    }

    #IgnoreCall(){
        videoSocket.send(JSON.stringify({type: 'ignore'})); 
    }
    

    #buildNotifier(){
        var _ = this;
        var buttons = (!_.isCaller)? [
                        {
                            title: "Answer",  
                            onclick: function(){ 
                                console.log("hello wolrd") 
                            } 
                        },
                        { 
                            title: "Ignore", 
                            onclick: function(){ 
                                _.#IgnoreCall()
                            } 
                        }
                    ] 
                : [
                    { 
                        title: "Ignore", 
                        onclick: function(){ 
                            _.#IgnoreCall()
                        } 
                    }
                ];
                
        popupMessage = new VideoPopup(
                        {
                            position: "top_right", 
                            title: (_.isCaller)? "Awaiting Answer": "Incomming Call", 
                            message: (_.isCaller)? "Awaiting answer from.": "Someone is calling you. would you like to answer.",
                            buttons: buttons
                        })

        popupMessage.build()
    }

   /* #sendSDPOffer(offer) {
        // Send SDP offer to the signaling server
        videoSocket.send(JSON.stringify({ type: 'offer', offer }));
    }

    #handleIceCandidate(event) {
        var _ = this;
        if (event.candidate) {
          // Send ICE candidate to the signaling server
          _.#sendICECandidate(event.candidate);
        }
    }

    #sendICECandidate(candidate) {
        // Send ICE candidate to the signaling server
        videoSocket.send(JSON.stringify({ type: 'ice-candidate', candidate }));
    }

    #handleRemoteStreamAdded(event) {
        document.getElementById("user-2").srcObject = event.streams[0];
    }


    #AddICECandidate(candidate) {
        // Handle ICE candidate from the other peer
        this.peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    }

    #handleSDPAnswer(answer) {
        // Handle SDP answer from the other peer
        this.peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
    }

    #handleSDPOffer(offer) {
        // Handle SDP offer from the other peer
        console.log(this.peerConnection)
        this.peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
        this.#createAnswer();
      }

    #createAnswer() {
        var _ = this;
        // Create SDP answer
        this.peerConnection.createAnswer().then(answer => {
            _.peerConnection.setLocalDescription(answer);
    
            // Send SDP answer to the signaling server
            _.#sendSDPAnswer(answer);
        });
    }

    #sendSDPAnswer(answer) {
        // Send SDP answer to the signaling server
        videoSocket.send(JSON.stringify({ type: 'answer', answer }));
      }
      */

    /*

    async #assignElm(){
        this.localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:false})
        document.getElementById("user-1").srcObject = this.localStream
    }

    async createOffer(){
        this.peerConnection = new RTCPeerConnection()

        this.remoteStream = new MediaStream()

        document.getElementById("user-2").srcObject = this.remoteStream
    }*/
}

var popupMessage= undefined