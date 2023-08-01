import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { HOST } from '../constant';

@Injectable({
  providedIn: 'root'
})
export class GenericService {
    constructor(private http: HttpClient) { }
}