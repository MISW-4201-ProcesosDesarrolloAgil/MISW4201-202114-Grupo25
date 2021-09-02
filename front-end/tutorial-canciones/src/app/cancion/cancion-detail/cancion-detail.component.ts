import { Component, OnInit, Input, Output, EventEmitter, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalComponent } from 'src/app/components/modal/modal.component';
import { ModalConfig } from 'src/app/components/modal/modal.config';
import { Cancion } from '../cancion';

@Component({
  selector: 'app-cancion-detail',
  templateUrl: './cancion-detail.component.html',
  styleUrls: ['./cancion-detail.component.css']
})
export class CancionDetailComponent implements OnInit {

  @ViewChild('modal') private modal: ModalComponent;

  @Input() cancion: Cancion;
  @Output() deleteCancion = new EventEmitter();

  userId: number;
  token: string;

  public modalConfig: ModalConfig = {
    modalTitle: 'Compartir Canción',
    dismissButtonLabel: 'Aceptar',
    closeButtonLabel: 'Cerrar',
    onDismiss: () => {
      console.log('Dismiss Modal');
      return true;
    },
    onClose: () => {
      console.log('Close Modal');
      return true;
    }
  };

  constructor(
    private router: ActivatedRoute,
    private routerPath: Router
  ) { }

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId)
    this.token = this.router.snapshot.params.userToken
  }

  eliminarCancion(){
    this.deleteCancion.emit(this.cancion.id)
  }

  goToEdit(){
    this.routerPath.navigate([`/canciones/edit/${this.cancion.id}/${this.userId}/${this.token}`])
  }

  async compartirCancion() {
    this.modalConfig.modalTitle = `Compartir Canción ${this.cancion.titulo}`;
    return await this.modal.open();
  }

}
