function editpost(id){
    fetch(`/edit/${id}`)
    .then(response => response.json())
    .then(blogpost =>{
        cardbody = document.querySelector(`#card-body-${id}`);
        cardbody.innerHTML = `<form id="editform-${blogpost.id}">
        <div class="form-group"><label for="textarea">Edit your post:</label>
        <textarea class="form-control" id="textarea-${blogpost.id}" rows="5">
        ${blogpost.body}</textarea><br><button class="btn btn-success btn-sm" type="submit">
        Save</button></form>`;
        const item = document.querySelector(`#editform-${blogpost.id}`);
        item.onsubmit = () => {
            const text = document.querySelector(`#textarea-${blogpost.id}`).value;
            fetch(`/edit/${blogpost.id}`, {
                method : 'PUT',
                body : JSON.stringify({
                    body : text,
                    username : blogpost.username
                })
            })
            showbody(`${blogpost.id}`);
            return false;
        }
    });
}

function showbody(id) {
        fetch(`/edit/${id}`)
    .then(response => response.json())
    .then(blogpost => {
        cardbody = document.querySelector(`#card-body-${id}`);
        // Print email
        cardbody.innerHTML = `<p>${blogpost.body}</p>`;
    });
}
