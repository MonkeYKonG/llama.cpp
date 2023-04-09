import React from 'react';

import { Container, CssBaseline } from '@mui/material';
import GlobalAppBar from './components/AppBar';
import Chat from './components/Chat';
import { AppContextProvider } from './context/AppContext';

function App() {
  return (
    <AppContextProvider>
      <Container>
        <CssBaseline />
        <GlobalAppBar />
        <Chat />
      </Container>
    </AppContextProvider>
  );
}

export default App;
