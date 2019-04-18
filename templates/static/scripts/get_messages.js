var message_list, update_interval;

function getMessages() {
  var msgReq = new XMLHttpRequest();
  msgReq.onreadystatechange = () => {
    if (msgReq.readyState == 4 && msgReq.status == 200) {
      updateDisplay(JSON.parse(msgReq.responseText));
    }
  }
  msgReq.open("POST", "/sys/update");
  msgReq.send("pls r dere new mesagz??");
}

function updateDisplay(message) {
  message_list.innerHTML += `
  <li>
    <span class="message-author">${message.author}</span>
    <span class="message-timestamp">${message.timestamp}</span>
    <span class="message-contents">${message.contents}</span>
  </li>
  `;
}

config.sysenv.onload_functions.push(() => {
  message_list = document.getElementById('message-list');
  update_interval = setInterval(getMessages, config.im_behavior.update_interval); // twice a second
});
