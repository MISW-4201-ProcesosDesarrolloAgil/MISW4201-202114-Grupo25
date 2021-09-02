import {
  Component,
  Injectable,
  Input,
  OnInit,
  TemplateRef,
  ViewChild,
} from '@angular/core';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ModalConfig } from './modal.config';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html'
})
@Injectable()
export class ModalComponent implements OnInit {
  @Input() public modalConfig: ModalConfig;
  @ViewChild('modal') private modalContent: TemplateRef<ModalComponent>;
  private modalRef: NgbModalRef;

  constructor(private modalService: NgbModal) {}

  ngOnInit(): void {}

  open(): Promise<boolean> {
    return new Promise<boolean>((resolve) => {
      this.modalRef = this.modalService.open(this.modalContent);
      this.modalRef.result.then(resolve, resolve);
    });
  }

  async close(): Promise<void> {
    const { shouldClose, onClose } = this.modalConfig;
    if (shouldClose === undefined || (await shouldClose())) {
      const result = onClose === undefined || (await onClose());
      this.modalRef.close(result);
    }
  }

  async dismiss(): Promise<void> {
    const { shouldDismiss, onDismiss } = this.modalConfig;
    if (shouldDismiss === undefined || (await shouldDismiss())) {
      const result = onDismiss === undefined || (await onDismiss());
      this.modalRef.dismiss(result);
    }
  }
}
