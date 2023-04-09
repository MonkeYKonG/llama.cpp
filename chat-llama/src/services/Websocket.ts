import { Socket, io } from "socket.io-client";

export default class SocketManager {
  static socket: Socket = io('http://localhost:8000');

  static reconnectSocket = () => {
    SocketManager.socket.disconnect();
    SocketManager.socket = io('http://localhost:8000');
  };

  static on: Socket['on'] = (eventName, callback) => SocketManager.socket.on(eventName, callback);
  static off: Socket['off'] = (eventName, callback) => SocketManager.socket.off(eventName, callback);

  static _emitEvent = (eventName: string, data: any = {}) => new Promise((resolve, reject) => {
    if (SocketManager.socket.connected === false) {
      reject(new Error('not connected'));
    }
    SocketManager.socket.emit(eventName, data, resolve);
  });

  static login = () => (
    SocketManager._emitEvent('login')
  );

  static initialize = () => (
    SocketManager._emitEvent('initialize')
  );

  static setHeader = (header: string) => (
    SocketManager._emitEvent('set-header', {
      header,
    })
  );

  static predict = (input: string) => (
    SocketManager._emitEvent('predict', {
      input,
    })
  );
}
