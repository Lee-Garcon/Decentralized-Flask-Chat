function sendMessage(text) {
  var errTimeout = setTimeout(() => {
    alert('Something went wrong whilst sending the message, is the server down?');
  }, config.im_behavior.send_server_timeout);

  var sendReq = new XMLHttpRequest();
  sendReq.onreadystatechange = () => {
    if (sendReq.readyState == 4 && sendReq.status == 200) {
      clearTimeout(errTimeout); // stop the client from yelling about stuff
    }
  }
  sendReq.open("POST", "/sys/send_message");
  sendReq.send();
}
