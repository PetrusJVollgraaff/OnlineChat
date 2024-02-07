var searchtimeout = undefined;

function searchUsers(elm, evt){
    var search = elm.value
    
    console.log(search)

	if(searchtimeout){
		clearTimeout(searchtimeout);
		searchtimeout = undefined;
	}
		
	searchtimeout = setTimeout(function(){
		if (evt.which == 13) {
			if (!(search == '')) {
                ShowSearchModal(search, elm)
    		}
		}
    },1000);
}

function ShowSearchModal(search, elm){
    fetch('/SearchUser', {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken"), },
        body: JSON.stringify({ search: search }),
    })
    .then((response) => { return response.json() })
    .then((data) => { 
        console.log(elm)
        console.log(elm.nextElementSibling)
        console.log( data.map(obj => {return `<option value='${obj.id}'>${obj.username}</option>`}).join('') )
        elm.nextElementSibling.innerHTML = data.map(obj => {return `<option value='${obj.id}'>${obj.username}</option>`}).join('')
        console.log(data)
    })
}