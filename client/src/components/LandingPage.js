import React from "react";
import styled from "styled-components";

import Paper from "./Paper";
import Output from "./Output";
import Navbar from "./Navbar";

const StyledLandingPage = styled(LandingPage)`
  display: grid;
  grid-template-columns: 1fr 4fr 4fr 1fr;
  grid-template-rows: 5vh 95vh;
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
    flex-direction: column;
    grid-row: 2;
    grid-column: 2 / 4;
  }
  .nav {
    grid-row: 1;
    grid-column: 1 / 5;
  }
`;
function LandingPage(props) {
  return (
    <div className={props.className}>
      <Navbar className="nav" />
      <div className="corner" />
      <Paper className="output-paper">
        <h2>Output #1</h2>
        <Output />
      </Paper>
    </div>
  );
}

export default StyledLandingPage;
