import { Injectable } from '@angular/core';
// import * as dgram from 'dgram'
import { WebsocketService } from './websocket.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UdpService {

  constructor(
    private webSocketService: WebsocketService
  ) { }


  createUdpClient(): Observable<any> {
    this.webSocketService.startConnection('ws://localhost:8080')

    return this.webSocketService.receive();
  }

  sendData(): void {
    this.webSocketService.send("hello world")
  }
}
