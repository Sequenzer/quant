const express = require("express");
const { spawn } = require("child_process");

const port = process.env.PORT || 5000;
const app = express();

app.get("/", (req, res) => {
  var dataToSend = "";
  const python = spawn("backTest/venv/Scripts/python", ["backTest/main.py"]);
  python.stdout.on("data", (data) => {
    console.log("Fetching data from Python");
    //console.log(data.toString());
    dataToSend = data.toString();
  });
  python.stderr.on("data", (error) => {
    console.log(error.toString());
  });
  python.on("close", (code) => {
    // console.log(`${code}`); if you want the closing code
    // respond to Browser
    res.send(dataToSend);
    console.log("closed");
  });
});

app.listen(port, () => console.log(`Server started on Port ${port}`));
