import React from "react";
import styled from "styled-components";

import Paper from "./Paper";
import Stockprice from "./Stockprice";
import Trades from "./Trades";
import Navbar from "./Navbar";

const StyledLandingPage = styled(LandingPage)`
  display: grid;
  grid-template-columns: 1fr 4fr 0.2fr 4fr 1fr;
  grid-template-rows: 10vh auto;
  h1 {
    background-color: ${(props) => props.theme.secondary};
    box-shadow: ${(props) => props.theme.outerShadow};
    color: ${(props) => props.theme.primary};
    padding: 0.5em;
    border-radius: 5px;
  }
  .corner {
    width: 500px;
    height: 100px;
    left: -150px;
    top: 50px;
    transform: rotate(-45deg);
    position: absolute;
    background-color: ${(props) => props.theme.secondary};
    filter: ${(props) => props.theme.dropShadow};
  }
  .output-paper {
    display: flex;
    align-items: stretch;
    flex-direction: column;
    justify-content: stretch;
  }
  .nav {
    grid-column: 1 / 6;
  }
  .output-header {
    text-align: center;
  }
  .otp1 {
    grid-column: 2 / 3;
  }
  .otp2 {
    grid-column: 4 / 5;
  }
  .inf1 {
    grid-column: 2 / 5;
  }
`;
function LandingPage(props) {
  return (
    <div className={props.className}>
      <Navbar className="nav" />
      <div className="corner" />
      <Paper className="output-paper otp1">
        <h2 className="output-header">Output #1</h2>
        <Stockprice />
      </Paper>
      <Paper className="output-paper otp2">
        <h2 className="output-header">Output #2</h2>
        <Trades />
      </Paper>
      <Paper className="output-paper inf1">
        <h2 className="output-header">Infobox</h2>
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
        eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
        voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet
        clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
        amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
        nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
        sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
        rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem
        ipsum dolor sit amet.
      </Paper>
    </div>
  );
}

export default StyledLandingPage;
