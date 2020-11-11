
function likepost(btn, postid) {
    const csrftoken = getCookie('csrftoken')
    fetch(`/like/${postid}`, {
        credentials : 'include',
        method : 'PUT',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    })
    .then(response => response.json())
    .then(result =>{
        if(result['message'] === "success") {
            let likes = parseInt(document.querySelector(`#likes-${postid}`).innerHTML);
            console.log(likes);
            if (btn.classList.contains("fa-heart")) {
                btn.classList.remove("fa-heart")
                btn.classList.add("fa-heart-o")
                likes--;
                console.log(likes);
                document.querySelector(`#likes-${postid}`).innerHTML = likes + " Likes";
            }else{
                btn.classList.remove("fa-heart-o")
                btn.classList.add("fa-heart")
                likes++;
                console.log(likes);
                document.querySelector(`#likes-${postid}`).innerHTML = likes + " Likes";
            }
        }
    })
}


function getCookie(name) {
    if (!document.cookie) {
      return null;
    }
    const token = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));

    if (token.length === 0) {
      return null;
    }
    return decodeURIComponent(token[0].split('=')[1]);
  };