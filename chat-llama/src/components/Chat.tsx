import React from "react";

import {
  Box,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import SendIcon from '@mui/icons-material/Send';

import AppBarHeader from "./AppBarHeader";
import { appBarHeight } from "../constants/AppBar";
import { textInputHeight } from "../constants/TextInput";

const a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

const Discussion: React.FC = () => (
  <List
    sx={{
      width: '100%',
      bgcolor: 'background.paper',
      position: 'relative',
      overflow: 'auto',
      height: '100%',
      // maxHeight: `calc(100vh - ${appBarHeight}px - ${textInputHeight}px)`,
      '& ul': { padding: 0 },
    }}
    subheader={<li />}
  >
    <ListItem>
      <ListItemText primary='Hello' />
    </ListItem>
    <ListItem>
      <ListItemText primary='Hello' />
    </ListItem>
    {
      a.map((b) => <ListItem key={b}><Typography>Hello!</Typography></ListItem>)
    }
  </List>
);

const TextInput: React.FC = () => (
  <Stack
    direction='row'
    alignItems='center'
    sx={{ mixHeight: '32px' }}
  >
    <TextField
      multiline
      sx={{ width: '100%' }}
    />
    <IconButton
      size='large'
    >
      <SendIcon />
    </IconButton>
  </Stack>
);

const Chat: React.FC = () => (
  <Stack
    direction='column'
    sx={{
      height: '100vh',
      padding: 2,
    }}
  >
    {/* <AppBarHeader /> */}
    <Stack
      justifyContent='space-between'
      direction='column'
      sx={{
        marginTop: `${appBarHeight}px`,
        maxHeight: `calc(100% - ${textInputHeight}px)`,
      }}
    >
      <Discussion />
      <TextInput />
    </Stack>
  </Stack>
);

export default Chat;
