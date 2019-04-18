const port = 3030;

const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.sendFile(__dirname + "/css_test.html");
});

app.use('/static', express.static(__dirname + "/../templates/static"));

app.listen(port, () => console.log('Listening on ' + port));
