const express = require("express");
const router = express.Router();

//OHLC Model
const OHLC = require("../../models/OHLC");

//@route 	Post api/data
//@desc 	Post a single OHLC datapoint
//@access 	Public

router.post("/", (req, res) => {
  console.log(req.body);
  const newOHLC = new OHLC({
    stock: req.body.stock,
    date: req.body.date,
    volume: req.body.volume,
    open: req.body.open,
    high: req.body.high,
    low: req.body.low,
    close: req.body.close,
    adjClose: req.body.adjClose,
  });
  OHLC.save()
    .then((OHLC) => res.json(OHLC))
    .catch((err) => console.log(err));

  res.send("Data Received...");
});

//@route 	GET api/data
//@desc 	Get dummy data
//@access 	Public

router.get("/OHLC", (req, res) => {
  if (req.query.stock) {
    OHLC.find({ stock: req.query.stock })
      .sort({ date: -1 })
      .then((OHLC) => {
        if (OHLC.length === 0) {
          res.json({
            msg: "No data found",
          });
          res.status(404);
        } else {
          res.json(OHLC);
        }
      })
      .catch((err) => console.log(err));
  } else {
    OHLC.find({ stock: "AAPL" })
      .sort({ date: -1 })
      .then((OHLC) => {
        if (OHLC.length === 0) {
          res.json({
            msg: "No data found",
          });
          res.status(404);
        } else {
          res.json(OHLC);
        }
      })
      .catch((err) => console.log(err));
  }
});

module.exports = router;
