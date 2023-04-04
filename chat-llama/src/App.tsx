import React from 'react';

import { Container, CssBaseline } from '@mui/material';
import GlobalAppBar from './components/AppBar';
import Chat from './components/Chat';

function App() {
  return (
    <Container    >
      <CssBaseline />
      <GlobalAppBar />
      <Chat />
    </Container>
  );
}

export default App;
