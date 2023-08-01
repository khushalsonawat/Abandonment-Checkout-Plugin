import { Component, OnInit} from '@angular/core';
import { GenericService } from '../services/generic.service';

@Component({
  selector: 'app-message-display',
  templateUrl: './message-display.component.html',
  styleUrls: ['./message-display.component.css'],
  providers: [GenericService]
})
export class MessageDisplayComponent implements OnInit {
    message : string;
    cart_id : string;

    constructor(
        private serviceObject:GenericService
    ){ }

    ngOnInit(): void {
        
    }
}
