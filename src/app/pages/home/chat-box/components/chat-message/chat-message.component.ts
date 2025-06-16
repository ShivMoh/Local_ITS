import { Component, Input, SimpleChanges } from '@angular/core';
import { Message } from '../../../../../models/message';
import { CommonModule, NgStyle } from '@angular/common';

@Component({
  selector: 'app-chat-message',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './chat-message.component.html',
  styleUrl: './chat-message.component.scss'
})
export class ChatMessageComponent {
  @Input() message: Message = new Message();
  userColor: string = "#88e788"
  agentColor: string = "#89E8A9"

  style: any = {
    backgroundColor: "blue"
  }

  ngOnChanges(simpleChanges: SimpleChanges) {
    if (this.message.type != "user") {
      this.style = {
        backgroundColor: this.agentColor,
        width: "80%",
        marginLeft: "50px"
      }
    } else {
      this.style = {
        backgroundColor: this.userColor,
        width: "80%"
      }
    }
  }

}
