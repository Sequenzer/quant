import { line } from "d3";
import React from "react";
import styled from "styled-components";

var bt = {
  id: "test",
  name: "test",
  start: "2017-01-01",
  end: "2017-01-01",
  strategy: "test",
  strategy_params: {
    test: "test",
  },
  data: {
    test: "test",
  },
  backtest: {
    test: "test",
  },
  results: {
    test: "test",
  },
  data: "Test",
};

function capFirstLetter(string) {
  return typeof string !== "string"
    ? "Not a string"
    : string.charAt(0).toUpperCase() + string.slice(1) + ":";
}

const StyledBacktestOutput = styled(BacktestOutput)`
  h2 {
    text-align: center;
  }
`;

function BacktestOutput(props) {
  function placeData(data) {}

  return (
    <div className={props.className}>
      <h2 className="output-paper otp1">Backtest</h2>
      <ul style={{ listStyleType: "none" }}>
        {Object.keys(bt).map((key) => {
          var otp = bt[key];
          if (typeof otp === "object") {
            // return (
            //   <li>
            //     <p>{key}</p>
            //     <p>"dummy"</p>
            //   </li>
            // );
          } else {
            return (
              <li key={key}>
                <StyledDataRow name={key} value={otp} />
              </li>
            );
          }
        })}
      </ul>
    </div>
  );
}

const StyledDataRow = styled(DataRow)`
  ::after {
    content: "";
    display: inline-block;
    padding-top: 1px;
    width: 100%;
    box-shadow: ${(props) => "0 -1px 0" + props.theme.secondary};
  }
  .content {
    height: 1rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }
  p {
    margin: 0;
  }
`;

function DataRow(props) {
  return (
    <div className={props.className}>
      <div className="content">
        <p>{capFirstLetter(props.name)}</p>
        <p>{props.value}</p>
      </div>
    </div>
  );
}

export default StyledBacktestOutput;
