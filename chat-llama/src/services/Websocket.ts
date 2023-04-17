import { Socket, io } from "socket.io-client";

interface LoginPayload { };

interface BaseConfigs {
  header: string;
  instruction: string;
  answer: string;
}

interface InitializePayload extends BaseConfigs { }

interface SetHeaderPayload extends BaseConfigs { }

interface PredictPayload { }

interface ResetPayload { }

export default class SocketManager {
  static socket: Socket = io('http://localhost:8000');

  static reconnectSocket = () => {
    SocketManager.socket.disconnect();
    SocketManager.socket = io('http://localhost:8000');
  };

  static on: Socket['on'] = (eventName, callback) => SocketManager.socket.on(eventName, callback);
  static off: Socket['off'] = (eventName, callback) => SocketManager.socket.off(eventName, callback);

  static _emitEvent = <T>(eventName: string, data: any = {}) => new Promise<T>((resolve, reject) => {
    if (SocketManager.socket.connected === false) {
      reject(new Error('not connected'));
    }
    SocketManager.socket.emit(eventName, data, resolve);
  });

  static login = () => (
    SocketManager._emitEvent<LoginPayload>('login')
  );

  static initialize = () => (
    SocketManager._emitEvent<InitializePayload>('initialize')
  );

  static setHeader = (
    header: string,
    instruction: string,
    answer: string,
  ) => (
    SocketManager._emitEvent<SetHeaderPayload>('set-header', {
      header,
      instruction,
      answer,
    })
  );

  static predict = (input: string) => (
    SocketManager._emitEvent<PredictPayload>('predict', {
      input,
    })
  );

  static reset = () => (
    SocketManager._emitEvent<ResetPayload>('reset', {})
  );
}
