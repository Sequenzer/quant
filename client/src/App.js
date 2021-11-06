import React from "react";
import { createGlobalStyle, ThemeProvider } from "styled-components";
import Poppins from "./assets/font/Poppins-Regular.ttf";
import StyledLandingPage from "./components/LandingPage";

const theme = {
  primary: "#F5F5F5",
  secondary: "#010D28",
  font: "poppins,sans-seriff",
  outerShadow:
    "0px 8px 8px rgba(0, 0, 0, 0.15), 0px 4px 4px rgba(0, 0, 0, 0.15), 0px 2px 2px rgba(0, 0, 0, 0.15), 0px 1px 1px rgba(0, 0, 0, 0.15)",
  innerShadow:
    "inset 0px 8px 8px rgba(0, 0, 0, 0.15), inset 0px 4px 4px rgba(0, 0, 0, 0.15), inset 0px 2px 2px rgba(0, 0, 0, 0.15), inset 0px 1px 1px rgba(0, 0, 0, 0.15)",
  dropShadow:
    "drop-shadow(0px 8px 8px rgba(0, 0, 0, 0.15)) drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.15)) drop-shadow(0px 2px 2px rgba(0, 0, 0, 0.15)) drop-shadow(0px 1px 1px rgba(0, 0, 0, 0.15))",
};

const GlobalStyle = createGlobalStyle`
@font-face {
    font-family: 'Poppins';
    src: url(${Poppins}) format('truetype');
    font-weight: 300;
    font-style: normal;
    font-display: auto;
  }
  body {
    font-family: ${(props) => props.theme.font};
    margin:0;
    
  }
  `;

function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <StyledLandingPage />
    </ThemeProvider>
  );
}

export default App;
