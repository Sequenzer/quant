import React from "react";
import styled from "styled-components";

function Paper(props) {
  return <div className={props.className}>{props.children}</div>;
}
const StyledPaper = styled(Paper)`
  background-color: ${(props) => props.theme.primary};
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.15), 4px 4px 4px rgba(0, 0, 0, 0.15),
    2px 2px 2px rgba(0, 0, 0, 0.15), 1px 1px 1px rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  padding: 2em;
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: center;
  margin: 1em;
`;

export default StyledPaper;
