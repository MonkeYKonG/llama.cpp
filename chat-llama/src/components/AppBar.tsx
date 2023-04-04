import { AppBar, Typography, styled } from "@mui/material";
import React from "react";
import { appBarHeight } from "../constants/AppBar";

const StyledAppBar = styled(AppBar, {})(({ theme }) => ({
  height: `${appBarHeight}px`,
  alignItems: 'start',
  justifyContent: 'center',
  padding: theme.spacing(2.5),
}));

const GlobalAppBar: React.FC = () => (
  <StyledAppBar>
    <Typography
      variant='h4'
    >
      Chat LLaMA
    </Typography>
  </StyledAppBar>
);

export default GlobalAppBar;
