import { Component, ElementRef, Input, Output, SimpleChange, SimpleChanges, ViewChild } from '@angular/core';
import { PdfViewerComponent, PdfViewerModule } from 'ng2-pdf-viewer';
import { FormsModule } from '@angular/forms';
import { FileService } from '../../../../services/file.service';
import { HttpClient } from '@angular/common/http';
import { EventEmitter } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-pdf-reader',
  standalone: true,
  imports: [
    PdfViewerModule,
    FormsModule,
    MatIconModule
  ],
  templateUrl: './pdf-reader.component.html',
  styleUrl: './pdf-reader.component.scss'
})
export class PdfReaderComponent {

  search_params: string = "basic";
  fileName: string = "session_3_rescued.pdf";
  pdfSrc: string = "";
  pageIndex: number = 0;
  @Input() relevantPages: any[] = [];
  pageNumber: number = 20;
  prompt = "";

  @Output() promptEmitter: EventEmitter<any> = new EventEmitter<any>();

  @ViewChild(PdfViewerComponent) private pdfComp!: PdfViewerComponent;

  constructor(
    private element: ElementRef,
    private fileService: FileService,
    private http: HttpClient
  ) {

  }

  ngOnInit() {
    this.fileService.getFile2(this.fileName).subscribe(file => {
      const fileURL = URL.createObjectURL(file);
      this.pdfSrc = fileURL;
    })
  }

  ngAfterViewInit() {
  }

  ngOnChanges(simpleChanges: SimpleChanges) {
    if (simpleChanges["relevantPages"]) {
      this.pageNumber = this.relevantPages[0].page;

      let items: string[] = this.relevantPages[0].source.split("/");
      let newFileName = items.pop();
      if (newFileName != this.fileName) {
        this.fileName = newFileName!;
        this.fileService.getFile2(this.fileName).subscribe(file => {
          const fileURL = URL.createObjectURL(file);
          this.pdfSrc = fileURL;
        })
      }

      console.log("The page number should be updating", this.pageNumber, this.relevantPages)

    }
  }
  ngOnUpdate(): void {
    // console.log("this is updating")
  }

  onFileSelected() {
    let $img: any = document.querySelector('#file');

    if (typeof (FileReader) !== 'undefined') {
      let reader = new FileReader();

      reader.onload = (e: any) => {
        this.pdfSrc = e.target.result;
      };

      reader.readAsArrayBuffer($img.files[0]);
    }
  }

  incrementPage() {

    this.pageIndex = this.pageIndex < this.relevantPages.length - 1 ? this.pageIndex + 1 : 0;

    let items: string[] = this.relevantPages[this.pageIndex].source.split("/");
    let newFileName = items.pop();

    // Shivesh writes: did i write this? or was it gpt? i don't think i'm this smart
    if (newFileName != this.fileName) {
      console.log(this.pageNumber, this.relevantPages)
      this.fileName = newFileName!;
      this.fileService.getFile2(this.fileName).subscribe(file => {
        const fileURL = URL.createObjectURL(file);
        this.pdfSrc = fileURL;
      })
      this.pageNumber = this.relevantPages[this.pageIndex].page;
    } else {
      console.log(this.pageNumber, this.relevantPages)
      this.pageNumber = this.relevantPages[this.pageIndex].page;
    }

    // console.log(this.pageNumber, this.relevantPages)
  }

  search(): void {
    console.log(this.search_params)
    this.pdfComp.eventBus.dispatch('find', {
      query: this.search_params,
      type: 'again',
      caseSensitive: false,
      findPrevious: undefined,
      highlightAll: true,
      phraseSearch: true
    })
  }

  searchFiles() {
    console.log("on pdf reader", this.prompt)
    this.promptEmitter.emit(
      {
        agent: "rag",
        prompt: this.prompt
      }
    );
  }


}
