import { Component, OnInit} from '@angular/core';
import { GenericService } from '../services/generic.service';
import { messageInfo } from './message';

@Component({
  selector: 'app-message-display',
  templateUrl: './message-display.component.html',
  styleUrls: ['./message-display.component.css'],
  providers: [GenericService]
})
export class MessageDisplayComponent implements OnInit {
    listOfMessages : Array<messageInfo>;
    displayedColumns: string[] = ['S.No.', 'Message' , 'Cart Token' ];

    constructor(
        private serviceObject:GenericService
    ){ }

    ngOnInit(): void {
        this.serviceObject.getData().subscribe({
            next:(data) => {
              this.listOfMessages = data;
            },
            error: (err) => {
              console.log(err);
            }
        });
    }
}
