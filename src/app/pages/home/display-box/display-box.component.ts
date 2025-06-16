import { Component, EventEmitter, Input, Output, SimpleChanges } from '@angular/core';
import { PdfReaderComponent } from './components/pdf-reader.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-display-box',
  standalone: true,
  imports: [
    PdfReaderComponent,
    CommonModule
  ],
  templateUrl: './display-box.component.html',
  styleUrl: './display-box.component.scss'
})
export class DisplayBoxComponent {
  @Input() fileType: string = "pdf";
  @Input() relevantDocuments: any

  @Output() promptEmitter : EventEmitter<any> = new EventEmitter<any>();

  metaData: any[] = [];
  documents: string[] = [];

  ngOnInit() {
    console.log("this works?")
  }

  ngOnChanges(simpleChanges: SimpleChanges) {
    if (simpleChanges["relevantDocuments"]) {
      if (this.relevantDocuments.length > 0) {

        this.metaData = this.relevantDocuments.map((doc: any) => {
          return { page: Number(doc.metaData.page_label), source: doc.metaData.source };
        })

        console.log("Relevant Documents", this.relevantDocuments)
      }

    }
  }

  emitPrompt(event : any) {
    console.log("On display box", event)
    this.promptEmitter.emit(event)
  }


}
