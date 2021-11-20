const express = require("express");
const { spawn } = require("child_process");
const router = express.Router();
const { PythonShell } = require("python-shell");
//OHLC Model
const OHLC = require("../../models/OHLC");

//@route 	GET api/backtesting/getbacktesting
//@desc 	Get a dummy Backtest
//@access 	Public

const pathToBacktest = "../backTest/main.py";
const pathToTemp = "../backTest/src/utils";

router.get("/", (req, res) => {
  var answer = "";

  //Interpret Input
  if (req.query.stock) {
    stockID = req.query.stock;
  } else {
    stockID = "AAPL";
  }
  OHLC.find({ stock: stockID })
    .sort({ date: -1 })
    .then((OHLC) => {
      if (Object.keys(OHLC).length === 0) {
        res.json({
          msg: "No data found",
        });
        res.status(404);
      } else {
        let options = {
          mode: "json",
          pythonPath: "../backTest/venv/Scripts/python",
          // pythonOptions: ["-u"], // get print results in real-time
          scriptPath: pathToTemp,
        };
        let pyshell = new PythonShell("toJSON.py", options);
        pyshell.send(OHLC);

        pyshell.on("message", function (message) {
          // received a message sent from the Python script (a simple "print" statement)
          // console.log(message);
          answer = message;
        });

        pyshell.end(function (err, code, signal) {
          if (err) throw err;
          console.log("The exit code was: " + code);
          console.log("The exit signal was: " + signal);

          res.send(answer);
          console.log("finished");
        });
      }
    })
    .catch((err) => {
      console.log(err);
    });
});

module.exports = router;
