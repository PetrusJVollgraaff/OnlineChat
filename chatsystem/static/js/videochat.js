class VideoChat{
    constructor(){

    }

    build(){

    }

    eventlistner(){

    }
}

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

        await this.#assignElm()
        this.#extraEvents()
    }

    eventlistner(){
        var _ = this;

        document.querySelector("#Call_Btn").addEventListener("click", function(){
            this.style.display = "none"
            _.#build()
        })
    }

    #extraEvents(){
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
        
        this.remoteStream = new MediaStream()

        document.getElementById("user-1").srcObject = this.localStream
    }
}