export class Message {
  id: string = "";
  type: string = ""; // user or llm
  content: string = "";
  time: string = ""; // date time stamp

  constructor() {
    this.id = "";
    this.type = "";
    this.content = "";
    this.time = "";
  }
}
