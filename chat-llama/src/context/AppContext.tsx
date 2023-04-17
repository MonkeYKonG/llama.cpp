import React, {
  createContext,
  useCallback,
  useEffect,
  useState,
} from "react";

import { DiscussionItem, Sources } from "../constants/Types";
import SocketManager from "../services/Websocket";

interface AppContextContent {
  isConnected: boolean;
  initialized: boolean;

  discussion: DiscussionItem[];
  currentlyGenerated?: DiscussionItem;
  addMessage: (target: Sources, text?: string) => void;
  reset: () => void;
  setOptions: (header: string, instruction: string, answer: string) => void;

  readyForInput: boolean;
  setReadyForInput: (readyForInput: boolean) => void;

  header: string;
  instructionPrefix: string;
  answerPrefix: string;
  setHeader: (header: string) => void;
  setInstructionPrefix: (instructionPRefix: string) => void;
  setAnswerPrefix: (answerPrefix: string) => void;
};

export const AppContext = createContext<AppContextContent>({
  isConnected: false,
  initialized: false,
  discussion: [],
  addMessage: () => { },
  reset: () => { },
  setOptions: () => { },
  readyForInput: false,
  setReadyForInput: () => { },
  header: '',
  instructionPrefix: '',
  answerPrefix: '',
  setHeader: () => { },
  setInstructionPrefix: () => { },
  setAnswerPrefix: () => { },
});

export const AppContextProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [discussion, setDiscussion] = useState<DiscussionItem[]>([]);
  const [currentlyGenerated, setCurrentlyGenerated] = useState<DiscussionItem>();
  const [connected, setConnected] = useState(false);
  const [initialized, setInitialized] = useState(false);
  const [readyForInput, setReadyForInput] = useState(true);
  const [header, setHeader] = useState('');
  const [instructionPrefix, setInstructionPrefix] = useState('');
  const [answerPrefix, setAnswerPrefix] = useState('');

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

  const reset = useCallback(() => {
    setDiscussion([]);
    setInitialized(false);
    SocketManager.reset()
      .then(() => {
        setInitialized(true);
      });
  }, []);

  const setOptions = useCallback((
    header: string,
    instruction: string,
    answer: string,
  ) => {
    setDiscussion([]);
    setInitialized(false);
    SocketManager.setHeader(header, instruction, answer)
      .then((result) => {
        setHeader(result.header);
        setInstructionPrefix(result.instruction);
        setAnswerPrefix(result.answer);
        setInitialized(true);
      });
  }, []);

  const handleSocketConnect = () => {
    SocketManager.initialize()
      .then((result) => {
        setInitialized(true);
        setHeader(result.header);
        setInstructionPrefix(result.instruction);
        setAnswerPrefix(result.answer);
      });
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
        reset,
        setOptions,
        readyForInput,
        setReadyForInput,
        header,
        instructionPrefix,
        answerPrefix,
        setHeader,
        setInstructionPrefix,
        setAnswerPrefix,
      }}
    >
      {children}
    </AppContext.Provider>
  )
};
