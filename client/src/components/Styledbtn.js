import React from "react";
import styled from "styled-components";

function Btn(props) {
  return <button className={props.className}>{props.children}</button>;
}

const StyledBtn = styled(Btn)`
  border: none;
  margin: 0 0.2em;
  font: inherit;
  cursor: pointer;
  outline: inherit;
  margin-right: ${(props) => (props.nomargin ? 0 : "3rem")};
  background-color: ${(props) =>
    props.selected ? props.theme.primary : "inherit"};
  padding: 7px 13px;
  border-radius: 5px;
  color: ${(props) => (props.selected ? "black" : "inherit")};
  text-decoration: inherit;
  user-select: none;
  &:focus,
  &:hover,
  &:visited,
  &:link,
  &:active {
    text-decoration: none;
  }
  :hover {
    background-color: ${(props) => props.theme.secondary};
    color: ${(props) => props.theme.primary};
  }
`;

export default StyledBtn;
