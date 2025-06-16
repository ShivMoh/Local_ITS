import { Component, Input, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { WebsocketService } from '../../../services/websocket.service';
import { Message } from '../../../models/message';
import { MessageService } from '../../../services/message.service';
import { CommonModule } from '@angular/common';
import { ChatMessageComponent } from './components/chat-message/chat-message.component';

@Component({
  selector: 'app-chat-box',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    ChatMessageComponent
  ],
  templateUrl: './chat-box.component.html',
  styleUrl: './chat-box.component.scss'
})
export class ChatBoxComponent {
  @Input() content = "";
  @Input() incomingMessage: boolean = false;
  @Input() newMessages: Message[] = [];
  messageQueue: Message[] = [

  ];


  constructor(
    private webSocketService: WebsocketService,
    private messageService: MessageService
  ) {

  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['incomingMessage']) {
      if (this.incomingMessage == true) {
        this.messageQueue = this.messageQueue.concat(this.newMessages);
        this.incomingMessage = false;
      }
    }
    if (changes['content']) {
      if (this.messageQueue.length > 0) {
        this.messageQueue[this.messageQueue.length - 1].content = this.content;
      }
    }
  }

  ngOnInit() {
    this.messageQueue = []
  }

  removeLastMessage() {
    this.messageQueue.pop();
  }


}
