import React from "react";
import styled from "styled-components";

import Btn from "./Styledbtn";

const StyledNavbar = styled(Navbar)`
  list-style-type: none;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
`;

function Navbar(props) {
  return (
    <ul className={props.className}>
      <li>
        <Btn>Home</Btn>
      </li>
      <li>
        <Btn>Run</Btn>
      </li>
      <li>
        <Btn>About</Btn>
      </li>
      <li>
        <Btn>Contact</Btn>
      </li>
    </ul>
  );
}

export default StyledNavbar;
