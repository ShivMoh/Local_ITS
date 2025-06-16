import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Config } from './common/config';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  constructor(private http: HttpClient) { }

  // get latest messages
  getFile(fileName: string): Observable<any> {
    return this.http.get<any>(`${Config.base_url}/pdfs/${fileName}`);
  }

  getFile2(fileName: string): Observable<any> {
    return this.http.get(`${Config.base_url}/file/pdfs/${fileName}`, { responseType: 'blob' });
  }

}
