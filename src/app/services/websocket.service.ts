import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  socket!: WebSocketSubject<any>;

  constructor() { }

  startConnection(url: string): void {
    this.socket = webSocket(url);
  }

  send(message: any): void {
    this.socket.next(message);
  }

  receive(): Observable<any> {
    return this.socket.asObservable();
  }

  close(): void {
    this.socket.complete();
  }
}
