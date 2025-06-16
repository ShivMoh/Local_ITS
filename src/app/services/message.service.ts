import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Message } from '../models/message';
import { Config } from './common/config';

@Injectable({
  providedIn: 'root'
})
export class MessageService {


  constructor(private http: HttpClient) { }

  // get latest messages
  getLatestMessages(count: number): Observable<Message[]> {
    return this.http.get<Message[]>(`${Config.base_url}/message/latest?count=${count}`);
  }


}
