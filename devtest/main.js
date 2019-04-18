const port = 3030;

const express = require('express');
const app = express();

app.use((req, res) => {
  console.log(`
${Date()}
    ${req.method} ${req.hostname} ${req.url}
    from ${req.ip}`);
    req.next();
});

app.get('/', (req, res) => {
  res.sendFile(__dirname + "/css_test.html");
});

app.use('/static', express.static(__dirname + "/../templates/static"));

app.listen(port, () => console.log('Listening on ' + port));
