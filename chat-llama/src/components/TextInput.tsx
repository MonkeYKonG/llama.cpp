import React, { useContext, useEffect, useState } from "react";

import {
  IconButton,
  Stack,
  TextField,
  styled,
} from "@mui/material";
import SendIcon from '@mui/icons-material/Send';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import DoneIcon from '@mui/icons-material/Done';

import { AppContext } from "../context/AppContext";
import SocketManager from "../services/Websocket";

const HiddenDiv = styled(Stack, {
  shouldForwardProp: (prop) => prop !== 'open'
})<{ open?: boolean }>(({ theme, open }) => ({
  maxHeight: '200px',
  overflow: 'auto',
  transition: theme.transitions.create(
    'max-height',
    {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }
  ),
  ...(!open && { maxHeight: '0px', overflow: 'hidden' })
}));

const TextInput: React.FC = () => {
  const {
    addMessage,
    setOptions,
    initialized,
    readyForInput,
    setReadyForInput,
    header,
    instructionPrefix,
    answerPrefix,
  } = useContext(AppContext);

  const [userInput, setUserInput] = useState('');
  const [optionsOpen, setOptionsOpen] = useState(false);
  const [headerInput, setHeaderInput] = useState('');
  const [instructionPrefixInput, setInstructionPrefixInput] = useState('');
  const [answerPrefixInput, setAnswerPrefixInput] = useState('');

  useEffect(() => {
    setHeaderInput(header);
  }, [header]);

  useEffect(() => {
    setInstructionPrefixInput(instructionPrefix);
  }, [instructionPrefix]);

  useEffect(() => {
    setAnswerPrefixInput(answerPrefix);
  }, [answerPrefix]);

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

  const toggleOptions = () => setOptionsOpen(!optionsOpen);

  const onHeaderInputChange: React.ChangeEventHandler<HTMLInputElement> = (event) => setHeaderInput(event.target.value);
  const onInstructionPrefixInputChange: React.ChangeEventHandler<HTMLInputElement> = (event) => setInstructionPrefixInput(event.target.value);
  const onAnswerPrefixInputChange: React.ChangeEventHandler<HTMLInputElement> = (event) => setAnswerPrefixInput(event.target.value);

  const onUpdateOptionsClick = () => {
    setOptions(headerInput, instructionPrefixInput, answerPrefixInput);
  };

  return (
    <Stack
      direction='column'
      spacing={1}
    >
      <HiddenDiv
        open={optionsOpen}
        direction='column'
        spacing={1}
      >
        <TextField
          label='Header'
          variant='filled'
          multiline
          sx={{ width: '100%' }}
          value={headerInput}
          onChange={onHeaderInputChange}
        />
        <Stack
          direction='row'
          spacing={1}
        >
          <TextField
            label='Instruction'
            variant='filled'
            multiline
            sx={{ width: '100%' }}
            value={instructionPrefixInput}
            onChange={onInstructionPrefixInputChange}
          />
          <TextField
            label='Answer'
            variant='filled'
            multiline
            sx={{ width: '100%' }}
            value={answerPrefixInput}
            onChange={onAnswerPrefixInputChange}
          />
          <IconButton
            onClick={onUpdateOptionsClick}
          >
            <DoneIcon />
          </IconButton>
        </Stack>
      </HiddenDiv>
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
        <IconButton
          onClick={toggleOptions}
        >
          <MoreHorizIcon />
        </IconButton>
      </Stack>
    </Stack>
  );
};

export default TextInput;
