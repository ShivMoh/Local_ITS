import { Component, ViewChild } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PdfViewerComponent } from 'ng2-pdf-viewer';
import { UdpService } from './services/udp.service';
import { WebsocketService } from './services/websocket.service';
import { ChatBoxComponent } from './pages/home/chat-box/chat-box.component';
import { PdfReaderComponent } from './pages/home/display-box/components/pdf-reader.component';
import { DisplayBoxComponent } from './pages/home/display-box/display-box.component';
// import { FileUploadComponent } from '../../server/home/shivesh/Documents/python/its_solution/local_its/src/app/pages/home/display-box/components/file-upload/file-upload.component';
import { Message } from './models/message';
import { InputBarComponent } from './pages/home/input-bar/input-bar.component';
import { AnimatedAgentComponent } from './pages/home/animated-agent/animated-agent.component';
import { HelpBoxComponent } from './pages/home/help-box/help-box.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    PdfReaderComponent,
    ChatBoxComponent,
    DisplayBoxComponent,
    InputBarComponent,
    AnimatedAgentComponent,
    HelpBoxComponent,
    CommonModule
    // FileUploadComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'local_its';
  content = "";
  helpContent = "";
  helpMessageIncoming : boolean = false;
  newMessageIncoming: boolean = false;
  requestingHelp: boolean = false;

  haveContext: boolean = false;
  context: any = "";
  messages: Message[] = [];
  prompt: string = "What is an operating system";

  updatesReady : boolean = false;

  @ViewChild(ChatBoxComponent) chatbox! : ChatBoxComponent;

  pages: number[] = [];

  constructor(
    private websocketService: WebsocketService
  ) {

  }


  ngOnInit() {
 
    this.websocketService.startConnection("ws://localhost:8080")

    this.websocketService.receive().subscribe((message) => {
      // console.log(message)
   
      if (message["agent"] == "riley") {
        if (!this.requestingHelp && this.helpContent.length <= 0) {
          console.log("Removing message");
          this.chatbox.removeLastMessage();
        }
        
        this.helpContent += message["message"];
        this.helpMessageIncoming = true;
        console.log("New message incoming", this.helpMessageIncoming)
        
      } else if (message["agent"] == "ruffle") {
        console.log("is this running?")

        this.content += message["message"];
      
      } else if (message["agent"] == "status") {
        console.log("STATUS UPDATE", message)
        this.updatesReady = true;
      } else {
        this.context = message["message"];
        this.haveContext = true;
      }
      

      this.newMessageIncoming = false;
    })
  }

  ngAfterViewInit() {
    this.send("I am a computer science tutor and I am here to help you learn. What would you like to learn about?")
  }

  update() {
    const message = {
      prompt: "Update Initated",
      agent: "dpo"
    };
    this.websocketService.send(message)
  }

  send(prompt: any, agent: string = "ruffle"): void {
    this.messages = [];
    this.haveContext = false;

    const message = {
      prompt: prompt,
      agent: agent
    };

    // TODO: having two different message formats is really bad and we should likely fix that sometime. Don't have the time rn tho
    this.messages.push({
      id: "",
      type: "user",
      content: message['prompt'],
      time: "sdjfjf"
    })

    this.content = "";
    this.websocketService.send(message)

    this.messages.push({
      id: "",
      type: agent,
      content: this.content,
      time: "sdjfja"
    })

    this.newMessageIncoming = true;
  }

  requestHelp(event: any) {
    this.helpContent = ""
    this.haveContext = false
    this.newMessageIncoming = false;
    this.websocketService.send(event);
  }

  requestDocuments(event: any) {
    this.helpContent = ""
    this.haveContext = false
    this.newMessageIncoming = false;
    this.websocketService.send(event);
    console.log("On app component ts", event)
  }

  updateHintState(event : boolean) {
    this.newMessageIncoming = event;
    this.helpContent = "";
    console.log("Updating new message incoming to", event);
  }

  updateHelpState(event : boolean) {
    this.requestingHelp = event;
  }

  removeLastMessage() {
    console.log(this.messages.length)
    this.chatbox.removeLastMessage();
    console.log(this.messages.length)
  }
}
