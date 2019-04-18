var default_config = {
  im_behavior: {
    update_interval: 500, // ms
    send_server_timeout: 3000 // miliseconds to wait before the client asks if the server is down
  },
  sysenv: {
    onload_functions: [],
    last_user: "undefined",
    curr_user: window.location.pathName.split('/', 3)[2]
  }
}

var config = default_config;

var confReq = new XMLHttpRequest();
confReq.onreadystatechange = () => {
  if (confReq.readyState == 4 && confReq.status == 200) {
    config = JSON.parse(confReq.responseText) || default_config;
  }
}
confReq.open('POST', '/sys/get_config');
confReq.send();

window.onload = () => {
  for (let func in config.sysenv.onload_functions) func();
}
