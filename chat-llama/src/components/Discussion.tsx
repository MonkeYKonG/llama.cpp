import React, { useContext, useEffect, useRef } from "react";

import {
  Box,
  CSSObject,
  Card,
  CardContent,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";
import { AppContext } from "../context/AppContext";

interface InputCardProps {
  content: string;
};

const boxMixins: CSSObject = {
  width: '100%',
  bgcolor: 'background.paper',
  position: 'relative',
  height: '100%',
}

const UserInputCard: React.FC<InputCardProps> = ({ content }) => (
  <Card>
    <CardContent>
      <Typography>You:</Typography>
      <Typography>{content}</Typography>
    </CardContent>
  </Card>
);

const ServerResponseCard: React.FC<InputCardProps> = ({ content }) => (
  <Card>
    <CardContent>
      <Typography>Server:</Typography>
      <Typography>{content}</Typography>
    </CardContent>
  </Card>
);

const Discussion: React.FC = () => {
  const {
    discussion,
    currentlyGenerated,
    isConnected,
    initialized,
  } = useContext(AppContext);
  const divRef = useRef<HTMLDivElement>();

  const scrollBottom = () => {
    if (divRef.current) {
      divRef.current.scrollTop = divRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    // TODO: Limit effect to only when already on bot
    scrollBottom();
  }, [divRef.current?.scrollHeight, discussion.length]);

  if (!isConnected || !initialized) {
    return (
      <Stack
        direction='column'
        sx={{
          ...boxMixins,
        }}
        alignItems='center'
        justifyContent='center'
        spacing={2}
      >
        <CircularProgress />
        <Typography>
          {
            !isConnected
              ? 'Connection to server...'
              : 'Initialize model...'
          }
        </Typography>
      </Stack>
    )
  }

  if (discussion.length === 0) {
    return (
      <Stack
        direction='column'
        sx={{
          ...boxMixins,
        }}
        alignItems='center'
        justifyContent='center'
      >
        <Typography>Hello how can I help you?</Typography>
      </Stack>
    )
  }

  return (
    <Box
      ref={divRef}
      sx={{
        ...boxMixins,
        overflow: 'auto',
        scrollBehavior: 'smooth',
        '& ul': { padding: 0 },
      }}
    >
      {
        discussion.map(({ source, text }, index) => (
          source === 'user'
            ? <UserInputCard key={index} content={text || ''} />
            : <ServerResponseCard key={index} content={text || ''} />
        ))
      }
      {
        currentlyGenerated
          ? <ServerResponseCard content={currentlyGenerated.text || ''} />
          : <></>
      }
    </Box>
  );
};

export default Discussion;
