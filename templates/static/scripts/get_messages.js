var update_interval = undefined;

function getMessages() {
  var msgReq = new XMLHttpRequest();
  msgReq.onreadystatechange = () => {
    if (msgReq.readyState == 4 && msgReq.status == 200) {
      msgReq.responseText = JSON.parse(msgReq.responseText);
      if (msgReq.responseText.author != config.sysenv.last_user) populateSidebar();
      updateDisplay(msgReq.responseText);
    }
  }
  msgReq.open("POST", "/sys/get_messages");
  msgReq.send("pls r dere new mesagz??");
}

function updateDisplay(message) {
  updateDisplay.list.innerHTML += `
  <li>
    <div>
      <span class="message-author">${message.author}</span>
      <span class="message-timestamp">${message.timestamp}</span>
      <span class="message-contents">${message.contents}</span>
    </div>
  </li>
  `;
}

config.sysenv.onload_functions.push(() => {
  updateDisplay.list = document.getElementById('message-list');
  update_interval = setInterval(getMessages, config.im_behavior.update_interval); // twice a second
});
