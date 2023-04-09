import React from "react";

import {
  Stack,
} from "@mui/material";

import { appBarHeight } from "../constants/AppBar";
import { textInputHeight } from "../constants/TextInput";
import Discussion from "./Discussion";
import TextInput from "./TextInput";



const Chat: React.FC = () => (
  <Stack
    direction='column'
    sx={{
      height: '100vh',
      padding: 2,
    }}
  >
    <Stack
      justifyContent='space-between'
      direction='column'
      sx={{
        marginTop: `${appBarHeight}px`,
        height: '100%',
        maxHeight: `calc(100% - ${textInputHeight}px)`,
      }}
    >
      <Discussion />
      <TextInput />
    </Stack>
  </Stack>
);

export default Chat;
