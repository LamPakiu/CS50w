document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#full").style.display = "none";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelectorAll("#hide").forEach(div => {
    div.style.display = 'none';
  })
  
  document.querySelector('#compose-form').onsubmit = () => {
    fetch("/emails",{
      method : "POST",
      body : JSON.stringify({
        recipients : document.querySelector('#compose-recipients').value,
        subject : document.querySelector('#compose-subject').value,
        body : document.querySelector('#compose-body').value,
      })
    })
    .then(response => response.json)
    .then(result => {
      console.log(result)
      load_mailbox('sent')
      return false;
    });
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails-contents').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#hide').style.display = 'block';
  document.querySelector("#full").style.display = "none";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = "";
  document.querySelector('#emails-contents').innerHTML = "";
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    for (let email of emails) {
      const newdiv = document.createElement('div');


      newdiv.innerHTML = `
        <div id="emailbox">
          <h5>From: ${email["sender"]}</h5>
          <h5>To: ${email["recipients"]}</h5>
          <div>Subject: ${email["subject"]}</div>
          <div>Timestamp: ${email["timestamp"]}</div>
        </div>
    `;

    newdiv.style.backgroundColor = 'white';

    if (email["read"]) {
      newdiv.style.backgroundColor = 'lightgrey';
    }
    else {
      newdiv.style.backgroundColor = 'white';
    }


    newdiv.addEventListener('click', () => load_email(email, mailbox));

    document.querySelector('#emails-contents').append(newdiv);

    };
    // ... do something else with emails ...
});

}

function archiving(email){
  fetch(`/emails/${email["id"]}`,{
    method: 'PUT',
    body: JSON.stringify({
        archived: !email["archived"]
    })
  })
  .then(() => load_mailbox("inbox"));
}

function load_email(email, mailbox) {
  document.querySelector("#full").style.display = "block";
  document.querySelector("#hide").style.display = "none";

  fetch(`/emails/${email["id"]}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })


  document.querySelector('#full').innerHTML = `
  <h2>From: ${email["sender"]} </h2>
  <h2>To: ${email["recipients"]} </h2>
  <h4>Subject: ${email["subject"]} </h4>
  <div class="text-muted"> Timestamp: ${email["timestamp"]} </div>
  <button class="btn btn-sm btn-outline-primary" id="archive">
  ${email["archived"] ? "Unarchive" : "Archive"}</button>
  <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
  <hr>
  <pre id="pre"> ${email["body"]} </pre>
  `;

  document.querySelector('#archive').addEventListener('click', () => {
    fetch(`/emails/${email["id"]}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !email["archived"]
      })
    })
      .then(() => load_mailbox("inbox"));
  });

  if (mailbox === 'sent'){
    document.querySelector('#archive').style.display = 'none';
  }

  document.querySelector('#reply').addEventListener('click', () =>{
    compose_email();

    if(email["subject"].slice(0,4) != "Re: "){
      email["subject"] = `Re: ${email["subject"]}`;
    }

    document.querySelector('#compose-recipients').value = email["sender"];
    document.querySelector('#compose-subject').value = `${email["subject"]}`;
    document.querySelector('#compose-body').value = `On ${email["timestamp"]}
    ${email["sender"]} wrote:\n
    ${email["body"]}
    `
  });

}



