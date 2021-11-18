const express = require("express");
const { spawn } = require("child_process");
const mongoose = require("mongoose");
const { csvToDb } = require("./utils/util");
var fs = require("fs");

const OHLC = require("./models/OHLC");

// For adding fiels to Db
// arr.forEach((file) => {
//   var name = file.slice(0, -4);
//   var count = 0;
//   OHLC.find({ stock: name }).exec(function (err, results) {
//     var count = results.length;
//     if (count == 0) {
//       //csvToDb(name);
//     } else {
//       console.log(count, name);
//     }
//   });
//   if (name !== "AAPL" && name !== "AXP") {
//     //For deleting
//     //OHLC.deleteMany({ stock: name }, (err, res) => console.log(err, res));
//     //csvToDb(name);
//     console.log("Finished", name);
//   }
// });

//csvToDb("BA");

//Import .env variables
require("dotenv").config();

const port = process.env.PORT || 5000;
const app = express();

//import routes
const data = require("./routes/api/data");
const bt = require("./routes/api/backtesting");

// Body parser middleware

app.use(express.json());
//DB Config
const db = process.env.MONGO_URI;

//Connect to MongoDB
mongoose
  .connect(db, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("MongoDB Connected..."))
  .catch((err) => console.log(err));

//Use Routes
app.use("/api/data", data);
app.use("/api/bt", bt);

app.listen(port, () => console.log(`Server started on Port ${port}`));
