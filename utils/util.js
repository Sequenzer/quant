const express = require("express");
const fs = require("fs");
const parse = require("csv-parse");

const OHLC = require("../models/OHLC");

function csvToDb(stock) {
  const pathToCsv = `./ressources/testData/${stock}.csv`;
  // Convert fs.readFile into Promise version of same
  const csvStringToJson = (csvString) => {
    const dataArr = csvString.split("\n");

    const header = dataArr[0].split(",");
    var solution = [];
    dataArr.map((ele, i) => {
      if (i > 0) {
        const datapointArr = ele.split(",");
        var newdp = {};
        header.forEach((head) => {
          newdp[head] = datapointArr[header.indexOf(head)];
        });
        solution.push(newdp);
      }
    });
    return solution;
  };
  const objToDB = (obj) => {
    obj.map((ele) => {
      if (ele.date !== undefined && ele.date !== "" && ele.date !== null) {
        const newOHLC = new OHLC({
          stock: stock,
          date: ele.date,
          open: ele.open,
          high: ele.high,
          low: ele.low,
          close: ele.close,
          volume: ele.volume,
          adjclose: ele.adjclose,
        });
        newOHLC
          .save()
          .then(() => console.log("Saved Datapoint"))
          .catch((err) => console.log(err, ele));
      }
    });
  };
  fs.readFile(pathToCsv, "utf8", (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    objToDB(csvStringToJson(data));
  });
}

module.exports = {
  csvToDb,
};
