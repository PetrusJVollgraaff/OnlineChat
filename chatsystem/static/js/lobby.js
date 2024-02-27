var searchtimeout = undefined;

function searchUsers(elm, evt){
    var search = elm.value

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
        elm.nextElementSibling.innerHTML = data.map(obj => {return `<div class="search_user_option" data-id='${obj.id}'>${obj.username}</div>`}).join('')
        elm.nextElementSibling.querySelectorAll(".search_user_option").forEach(function(searchuser){
            searchuser.onclick = function(e){
                OpenSearchSelect(this.dataset.id);
            }
        });
    })
}

function OpenSearchSelect(searchid){
    fetch('/SearchOpen', {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken"), },
        body: JSON.stringify({ searchid: searchid }),
    })
}