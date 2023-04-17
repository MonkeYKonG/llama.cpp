import React, { useContext } from "react";

import {
  AppBar,
  IconButton,
  Stack,
  Typography,
  styled,
} from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

import { appBarHeight } from "../constants/AppBar";
import { AppContext } from '../context/AppContext';

const StyledAppBar = styled(AppBar, {})(
  ({ theme }) => ({
    height: `${appBarHeight}px`,
    justifyContent: 'center',
    padding: theme.spacing(2.5),
  })
);

const GlobalAppBar: React.FC = () => {
  const { reset } = useContext(AppContext);

  return (
    <StyledAppBar>
      <Stack
        direction='row'
        justifyContent='space-between'
      >
        <Typography
          variant='h4'
        >
          Chat LLaMA
        </Typography>
        <IconButton
          onClick={reset}
        >
          <DeleteIcon />
        </IconButton>
      </Stack>
    </StyledAppBar >
  );
};

export default GlobalAppBar;
