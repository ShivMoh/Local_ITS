import { Component, Input, Output, SimpleChanges } from '@angular/core';
import { Message } from '../../../models/message';
import { EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-help-box',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatTooltipModule
  ],
  templateUrl: './help-box.component.html',
  styleUrl: './help-box.component.scss'
})
export class HelpBoxComponent {
  @Input() content: string = "";
  @Output() messageEmitter: EventEmitter<any> = new EventEmitter<any>()
  @Output() answerStateEmitter : EventEmitter<boolean> = new EventEmitter<boolean>(false);
  @Output() helpStateEmitter : EventEmitter<boolean> = new EventEmitter<boolean>(false);
  @Input() requestingHelp : boolean = false;
  answered: boolean = false;
 
  constructor() {

  }

  ngOnChanges(changes: SimpleChanges) {

    if (changes['content']) {
      console.log("changes are happening")
      if (this.content.length > 0) {
        this.answered = true;
        console.log("Answered is currently", this.answered)

      }
    }
  }

  closeRileyHint() {
    this.answered = false;
    this.content = "";  
    this.requestingHelp = false;
    this.helpStateEmitter.emit(this.requestingHelp);
    
    this.answerStateEmitter.emit(this.answered);

  }

  requestRileyHelp() {
    this.content = "";
    this.answered = true;
    this.requestingHelp = true;
    this.helpStateEmitter.emit(this.requestingHelp);

    this.messageEmitter.emit(
      {
        agent: "riley",
        prompt: ""
      }
    );

  }
}
