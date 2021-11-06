const express = require("express");
const { spawn } = require("child_process");
const router = express.Router();

//@route 	GET api/backtesting/getbacktesting
//@desc 	Get a dummy Backtest
//@access 	Public

router.get("/", (req, res) => {
  var dataToSend = "";
  const python = spawn("../backTest/venv/Scripts/python", [
    "../backTest/main.py",
  ]);
  python.stdout.on("data", (data) => {
    console.log("Fetching data from Python");
    console.log(data.toString());
    dataToSend = data.toString();
  });
  python.stderr.on("data", (error) => {
    console.log(error.toString());
  });
  python.on("close", (code) => {
    res.send(dataToSend);
    console.log("closed");
  });
});

module.exports = router;
