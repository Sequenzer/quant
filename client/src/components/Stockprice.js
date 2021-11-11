import React, { useEffect } from "react";
import * as d3 from "d3";
import axios from "axios";

const heightValue = 400;
const widthValue = 800;
const pad = { left: 30, right: 5, top: 5, bottom: 20 };

const url_ohlc = "/api/data/OHLC";

function Stockprice(props) {
  useEffect(() => onMount(), []);

  function getData(stock) {
    var sol = [];
    axios
      .get(url_ohlc, {
        params: {
          stock: stock,
        },
      })
      .then((res) => {
        res.data.forEach((element) => {
          sol.push({
            date: new Date(element.date),
            close: element.close,
            open: element.open,
            high: element.high,
            low: element.low,
          });
        });
      })
      .then(() => {
        console.log(sol[0]);
        //Cut Data
        var cut = sol.slice(0, 50);
        drawChart(cut);
      })
      .then(() => {
        console.log("Done drawing chart");
      });
  }

  const drawChart = (data) => {
    //Get bound of the axis
    const date_bound = [
      d3.min(d3.map(data, (d) => d.date)),
      d3.max(d3.map(data, (d) => d.date)),
    ];
    const close_bound = [
      d3.min(d3.map(data, (d) => d.close)),
      d3.max(d3.map(data, (d) => d.close)),
    ];

    const svg = d3.select("#data_svg");

    //Init Scales
    var xScale = d3
      .scaleTime()
      .domain(date_bound)
      .range([pad.left, widthValue]);
    var yScale = d3
      .scaleLinear()
      .domain(close_bound)
      .range([heightValue, pad.top])
      .nice();

    //Add X axis
    var xAxis = svg
      .append("g")
      .attr("transform", "translate(0," + heightValue + ")")
      .call(d3.axisBottom(xScale));
    // Add Y axis
    var yAxis = svg
      .append("g")
      .attr("transform", "translate(" + pad.left + ",0)")
      .call(d3.axisLeft(yScale));
    // Add the data
    var plt = svg.append("g").attr("clip-path", "url(#clip)");

    function drawCandle(parent, data, width) {
      var boxHeight = yScale(data.close) - yScale(data.open);

      var candles = parent
        .append("g")
        .classed("ohlc", true)
        .selectAll("box")
        .data(data)
        .enter()
        .append("g");

      candles
        .append("rect")
        .attr("x", (d) => xScale(d.date.setHours(0, 0, 0, 0)) - width / 2)
        .attr("y", (d) => yScale(Math.max(d.open, d.close)))
        .attr("width", width)
        .attr("height", (d) => Math.abs(yScale(d.open) - yScale(d.close)))
        .attr("fill", (d) => (d.open > d.close ? "red" : "green"))
        .append("text")
        .text((d) => d.open + " - " + d.close);

      candles
        .append("line")
        .attr("x1", (d) => xScale(d.date))
        .attr("y1", (d) => yScale(d.low))
        .attr("x2", (d) => xScale(d.date))
        .attr("y2", (d) => yScale(d.high))
        .attr("stroke", "black");
    }

    drawCandle(plt, data, (widthValue - pad.left) / data.length);

    // Add brushing
    var brush = d3
      .brushX() // Add the brush feature using the d3.brush function
      .extent([
        [0, 0],
        [widthValue, heightValue],
      ]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
      .on("end", updateChart); // Each time the brush selection changes, trigger the 'updateChart' function

    //append brushing
    plt.append("g").attr("class", "brush").call(brush);

    function updateChart(event) {
      var extent = event.selection;
      //if no selection is made back to init coords
      if (!extent) {
        if (!idleTimeout) return (idleTimeout = setTimeout(idled, 350)); // This allows to wait a little bit
        xScale.domain([4, 8]);
      } else {
        var mindate = xScale.invert(extent[0]);
        var maxdate = xScale.invert(extent[1]);
        xScale.domain([
          mindate.setHours(0, 0, 0, 0),
          maxdate.setHours(0, 0, 0, 0),
        ]);
        yScale.domain([
          d3.min(data, (d) => {
            if (d.date > mindate && d.date < maxdate) {
              return Math.min(d.low, d.open, d.close);
            }
          }),
          d3.max(data, (d) => {
            if (d.date > mindate && d.date < maxdate) {
              return Math.max(d.high, d.open, d.close);
            }
          }),
        ]);
        plt.select(".brush").call(brush.move, null); // This remove the grey brush area as soon as the selection has been done
      }
      // Update axis and line position
      xAxis.transition().duration(1000).call(d3.axisBottom(xScale));
      yAxis.transition().duration(1000).call(d3.axisLeft(yScale));

      //Remove Object outside of scale

      var candlestoRemove = plt.select(".ohlc").selectAll("g");

      candlestoRemove
        .filter((d) => {
          return xScale(d.date) < 0 || xScale(d.date) > widthValue;
        })
        .remove();

      updateCandles(plt);

      function updateCandles(plt) {
        // Update the the candle positions
        var candle = plt.select(".ohlc").selectAll("g");
        //get selection length
        var blockwidth = (widthValue - pad.left) / xScale.ticks().length;
        console.log(blockwidth, candle.size(), xScale.ticks().length);

        candle
          .select("rect")
          .transition()
          .duration(1000)
          .attr("x", (d) => xScale(d.date) - blockwidth / 2)
          .attr("y", (d) => yScale(Math.max(d.open, d.close)))
          .attr("height", (d) => Math.abs(yScale(d.open) - yScale(d.close)))
          .attr("width", blockwidth);

        candle
          .select("line")
          .transition()
          .duration(1000)
          .attr("x1", (d) => xScale(d.date))
          .attr("x2", (d) => xScale(d.date))
          .attr("y1", (d) => yScale(d.low))
          .attr("y2", (d) => yScale(d.high));
      }

      //on dbClick action
      svg.on("dblclick", function () {
        //First Redraw then reScale

        xScale.domain(d3.extent(data, (d) => d.date));
        yScale.domain(d3.extent(data), (d) => d.close);
        xAxis.transition().call(d3.axisBottom(xScale));
        yAxis.transition().call(d3.axisLeft(yScale));
      });
    }
    // gridlines in y axis function
    function make_y_gridlines() {
      return d3.axisLeft(yScale).ticks(3);
    }

    // add the Y gridlines
    var yGrid = svg
      .append("g")
      .attr("class", "grid")
      .attr("transform", "translate(" + pad.left + ",0)")
      .call(make_y_gridlines().tickSize(-widthValue).tickFormat(""));
  };

  // A function that set idleTimeOut to null
  var idleTimeout;
  function idled() {
    idleTimeout = null;
  }

  const onMount = () => {
    //get Data from APi
    var data = getData("GOOG");

    //d3.select("#data_svg_root").style("grid-row", "2");

    var svg = d3
      .select("#data_svg_root")
      .append("svg")
      .attr("id", "data_svg")
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr(
        "viewBox",
        `0 0 ${widthValue + pad.left + pad.right} ${
          heightValue + pad.top + pad.bottom
        }`
      )
      .style("border-radius", "5px");

    // Add a clipPath: everything out of this area won't be drawn.
    var clip = svg
      .append("defs")
      .append("svg:clipPath")
      .attr("id", "clip")
      .append("svg:rect")
      .attr("width", widthValue - pad.left)
      .attr("height", heightValue)
      .attr("x", pad.left)
      .attr("y", 0);
  };

  return <div id="data_svg_root"></div>;
}

export default Stockprice;
