var default_config = {
  im_behavior: {
    update_interval: 500 // ms
  }
}

var config = {};

var confReq = new XMLHttpRequest();
confReq.onreadystatechange = () => {
  if (confReq.readyState == 4 && confReq.status == 200) {
    config = JSON.parse(confReq.responseText) || default_config;
  }
}
confReq.open('POST', '/sys/get_config');
confReq.send();
