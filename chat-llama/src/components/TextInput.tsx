import React, { useContext, useState } from "react";

import {
  IconButton,
  Stack, TextField,
} from "@mui/material";
import SendIcon from '@mui/icons-material/Send';
import { AppContext } from "../context/AppContext";
import SocketManager from "../services/Websocket";


const TextInput: React.FC = () => {
  const {
    addMessage,
    initialized,
    readyForInput,
    setReadyForInput,
  } = useContext(AppContext);

  const [userInput, setUserInput] = useState('');

  const inputDisabled = !initialized || !readyForInput;

  const onSendClick = () => {
    if (userInput === '') return;

    addMessage('user', userInput);
    SocketManager.predict(userInput);
    setUserInput('');
    setReadyForInput(false);
  };

  const keyDownHandler: React.KeyboardEventHandler = (event) => {
    if (event.ctrlKey && event.code === 'Enter') {
      onSendClick();
    }
  }

  return (
    <Stack
      direction='row'
      alignItems='center'
      spacing={1}
    >
      <TextField
        multiline
        maxRows={6}
        sx={{
          width: '100%',
        }}
        value={userInput}
        onChange={(event) => setUserInput(event.target.value)}
        onKeyDown={keyDownHandler}
        disabled={inputDisabled}
      />
      <IconButton
        size='large'
        onClick={onSendClick}
        disabled={inputDisabled}
      >
        <SendIcon />
      </IconButton>
    </Stack>
  );
};

export default TextInput;
