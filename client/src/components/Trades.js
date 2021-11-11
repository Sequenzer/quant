import React, { useEffect } from "react";
import * as d3 from "d3";
import axios from "axios";
import Stockprice from "./Stockprice";

const heightValue = 400;
const widthValue = 800;
const pad = { left: 30, right: 5, top: 5, bottom: 20 };

const url_ohlc = "/api/data/OHLC";

function Trades(props) {
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
          });
        });
      })
      .then(() => {
        drawChart(sol);
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

    const svg = d3.select("#trades_svg");

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
    // Add the line
    var line = svg.append("g").attr("clip-path", "url(#clip)");

    var series = line.append("g").classed("series", true);
    series
      .append("path")
      .datum(data)
      .attr("class", "line") // I add the class line to be able to modify this line later on.
      .attr("fill", "none")
      .attr("stroke", "green")
      .attr("stroke-width", 1.5)
      .attr(
        "d",
        d3
          .line()
          .x((d) => {
            //console.log(xScale(d.close));
            return xScale(d.date);
          })
          .y((d) => {
            //console.log(yScale(d.close));
            return yScale(d.close);
          })
      );

    // Add brushing
    var brush = d3
      .brushX() // Add the brush feature using the d3.brush function
      .extent([
        [0, 0],
        [widthValue, heightValue],
      ]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
      .on("end", updateChart); // Each time the brush selection changes, trigger the 'updateChart' function

    //append brushing
    line.append("g").attr("class", "brush").call(brush);

    function updateChart(event) {
      var extent = event.selection;
      //if no selection is made back to init coords
      if (!extent) {
        if (!idleTimeout) return (idleTimeout = setTimeout(idled, 350)); // This allows to wait a little bit
        xScale.domain([4, 8]);
      } else {
        xScale.domain([xScale.invert(extent[0]), xScale.invert(extent[1])]);
        line.select(".brush").call(brush.move, null); // This remove the grey brush area as soon as the selection has been done
      }
      // Update axis and line position
      xAxis.transition().duration(1000).call(d3.axisBottom(xScale));
      line
        .select(".line")
        .transition()
        .duration(1000)
        .attr(
          "d",
          d3
            .line()
            .x((d) => {
              //console.log(d.date);
              return xScale(d.date);
            })
            .y((d) => {
              //console.log(d.close);
              return yScale(d.close);
            })
        );
      //on dbClick action
      svg.on("dblclick", function () {
        xScale.domain(d3.extent(data, (d) => d.date));
        xAxis.transition().call(d3.axisBottom(xScale));
        line
          .select(".line")
          .transition()
          .attr(
            "d",
            d3
              .line()
              .x((d) => xScale(d.date))
              .y((d) => yScale(d.close))
          );
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
      .select("#trades_svg_root")
      .append("svg")
      .attr("id", "trades_svg")
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

  return <div id="trades_svg_root"></div>;
}

export default Trades;
