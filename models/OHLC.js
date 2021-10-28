const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const OHLCSchema = new Schema({
  stock: {
    type: String,
    required: true,
  },
  date: {
    type: Date,
    default: Date.now,
    required: true,
  },
  volume: {
    type: Number,
    default: 0,
  },
  open: {
    type: Number,
    default: 0,
  },
  high: {
    type: Number,
    default: 0,
  },
  low: {
    type: Number,
    default: 0,
  },
  close: {
    type: Number,
    default: 0,
  },
  adjclose: {
    type: Number,
    default: 0,
  },
});

module.exports = Item = mongoose.model("OHLC", OHLCSchema);
