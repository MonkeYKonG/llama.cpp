import React, { createContext, useCallback, useEffect, useMemo, useState } from "react";

import { DiscussionItem, Sources } from "../constants/Types";
import SocketManager from "../services/Websocket";

interface AppContextContent {
  isConnected: boolean;
  initialized: boolean;

  discussion: DiscussionItem[];
  currentlyGenerated?: DiscussionItem;
  addMessage: (target: Sources, text?: string) => void;

  readyForInput: boolean;
  setReadyForInput: (readyForInput: boolean) => void;
};

export const AppContext = createContext<AppContextContent>({
  isConnected: false,
  initialized: false,
  discussion: [],
  addMessage: () => { },
  readyForInput: false,
  setReadyForInput: () => { },
});

export const AppContextProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [discussion, setDiscussion] = useState<DiscussionItem[]>([]);
  const [currentlyGenerated, setCurrentlyGenerated] = useState<DiscussionItem>();
  const [connected, setConnected] = useState(false);
  const [initialized, setInitialized] = useState(false);
  const [readyForInput, setReadyForInput] = useState(true);

  const addMessage = useCallback((source: Sources, text?: string) => {
    console.log('add message', discussion);
    setDiscussion([
      ...discussion,
      {
        source,
        text,
      }
    ])
  }, [discussion]);

  const handleSocketConnect = () => {
    SocketManager.initialize()
      .then(() => { setInitialized(true) });
    setConnected(true);
  };

  const handleSocketDisconnect = () => {
    setConnected(false);
    setInitialized(false);
  };

  const handleStartPrediction = useCallback(() => {
    setReadyForInput(false);
    setCurrentlyGenerated({
      source: 'server',
      text: '',
    });
  }, []);

  const handleStopPrediction = useCallback(() => {
    setReadyForInput(true);
    setCurrentlyGenerated(undefined);
    addMessage('server', currentlyGenerated?.text);
  }, [currentlyGenerated, addMessage]);

  const handlePredicted = useCallback(({ next_str: nextStr }: { next_str: string }) => {
    console.log('Predicted', nextStr);
    setCurrentlyGenerated({
      source: 'server',
      text: (currentlyGenerated?.text || '') + nextStr,
    });
  }, [currentlyGenerated]);

  useEffect(() => {
    SocketManager.on('connect', handleSocketConnect);
    SocketManager.on('disconnect', handleSocketDisconnect);

    return () => {
      SocketManager.off('connect', handleSocketConnect);
      SocketManager.off('disconnect', handleSocketDisconnect);
    }
  }, []);

  useEffect(() => {
    SocketManager.on('start-prediction', handleStartPrediction);
    SocketManager.on('stop-prediction', handleStopPrediction);
    SocketManager.on('predicted', handlePredicted);

    return () => {
      SocketManager.off('start-prediction', handleStartPrediction);
      SocketManager.off('stop-prediction', handleStopPrediction);
      SocketManager.off('predicted', handlePredicted);
    }
  }, [handleStartPrediction, handleStopPrediction, handlePredicted]);

  return (
    <AppContext.Provider
      value={{
        isConnected: connected,
        initialized,
        discussion,
        currentlyGenerated,
        addMessage,
        readyForInput,
        setReadyForInput,
      }}
    >
      {children}
    </AppContext.Provider>
  )
};
