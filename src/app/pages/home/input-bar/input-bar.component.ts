import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-input-bar',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './input-bar.component.html',
  styleUrl: './input-bar.component.scss'
})
export class InputBarComponent {

  prompt: string = "What is an operating system";
  @Output() promptEmitter: EventEmitter<string> = new EventEmitter<string>();

  ngOnUpdate() {
    console.log("this is the current prompt")
  }
  sendPrompt() {
    this.promptEmitter.emit(this.prompt);

    // reset prompt
    this.prompt = "";
  }

}
