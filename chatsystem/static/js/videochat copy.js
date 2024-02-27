class VideoSystem{
    constructor(){
        this.peerConnection = undefined
        this.localStream    = undefined
        this.remoteStream   = undefined
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
            _.#build()

            videoSocket.send(JSON.stringify({type: 'call'}));
        })

        videoSocket.onmessage = function (event) {
            console.log(event)
            const data = JSON.parse(event.data);
            console.log(data)
            if(type == 'call_received') {
                // console.log(response);
                onNewCall(response.data)
            }
    
            if(type == 'call_answered') {
                onCallAnswered(response.data);
            }
            
            if (data.message.type == 'offer') {
                // Received SDP offer from the other peer
                _.#handleSDPOffer(data.message.offer);
            } else if (data.message.type == 'answer') {
                // Received SDP answer from the other peer
                _.#handleSDPAnswer(data.message.answer);
            } else if (data.message.type == 'ice-candidate') {
                // Received ICE candidate from the other peer
                _.#handleICECandidate(data.message.candidate);
            }
        };
    }

    async startScreenSharing() {
        try {
            const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: true });
            localVideo.srcObject = screenStream;
    
            // Add screen stream to peer connection
            screenStream.getTracks().forEach(track => peerConnection.addTrack(track, screenStream));
    
            // Create and send SDP offer
            createOffer();
        } catch (error) {
            console.error('Error starting screen sharing:', error);
        }
    }


    async #getStreamVar(){
        var _ = this;

        this.#build()
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


    #createPeerConnection() {
        var _ = this
        this.peerConnection = new RTCPeerConnection();
    
        // Add local stream to peer connection
        _.localStream.getTracks().forEach(track => _.peerConnection.addTrack(track, _.localStream));
        console.log("hello")
        // Set up event handlers for ICE negotiation
        _.peerConnection.onicecandidate = this.#handleIceCandidate;
        _.peerConnection.ontrack = this.#handleRemoteStreamAdded;
    }

    async #createOffer() {
        try {
          const offer = await this.peerConnection.createOffer();
          await this.peerConnection.setLocalDescription(offer);
      
          // Send offer to the signaling server
          this.#sendSDPOffer(offer);
        } catch (error) {
          console.error('Error creating offer:', error);
        }
    }

    #sendSDPOffer(offer) {
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


    #handleICECandidate(candidate) {
        // Handle ICE candidate from the other peer
        peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    }

    #handleSDPAnswer(answer) {
        // Handle SDP answer from the other peer
        peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
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

    /*#extraEvents(){
        var _ = this
        console.log("world")
        document.querySelector("#End_Btn").addEventListener("click", function(){
            _.localStream = undefined
            document.querySelector(".main_ctn[data-t='both']").setAttribute('data-t', 'chat')
            document.getElementById("video_ctn").innerHTML = ""
            document.querySelector("#Call_Btn").style.display = ""
        })
    }

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