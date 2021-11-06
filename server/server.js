const express = require("express");
const { spawn } = require("child_process");
const mongoose = require("mongoose");
const { csvToDb } = require("./utils/util");

//csvToDb("AAPL");

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
