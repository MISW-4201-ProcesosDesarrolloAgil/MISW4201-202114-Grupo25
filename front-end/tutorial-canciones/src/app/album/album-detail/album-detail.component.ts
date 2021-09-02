import {
  Component,
  Input,
  OnInit,
  Output,
  EventEmitter,
  ViewChild,
} from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AlbumService } from '../album.service';
import { Album, Cancion } from '../album';

import { ModalComponent } from 'src/app/components/modal/modal.component';
import { ModalConfig } from 'src/app/components/modal/modal.config';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.scss'],
})
export class AlbumDetailComponent implements OnInit {
  @ViewChild('modal') private modal: ModalComponent;

  @Input() album: Album;
  @Output() deleteAlbum = new EventEmitter();

  comentarioForm: FormGroup;
  comentario: string;

  userId: number;
  token: string;

  public modalConfig: ModalConfig = {
    modalTitle: 'Agregar Comentario a Álbum'
  };

  constructor(
    private routerPath: Router,
    private router: ActivatedRoute,
    private albumService: AlbumService,
    private toastr: ToastrService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId);
    this.token = this.router.snapshot.params.userToken;
    this.comentarioForm = this.formBuilder.group({
      comentario: ['', [Validators.required, Validators.maxLength(1000)]],
    });
  }

  goToEdit() {
    this.routerPath.navigate([
      `/albumes/edit/${this.album.id}/${this.userId}/${this.token}`,
    ]);
  }

  goToJoinCancion() {
    this.routerPath.navigate([
      `/albumes/join/${this.album.id}/${this.userId}/${this.token}`,
    ]);
  }

  eliminarAlbum() {
    this.deleteAlbum.emit(this.album.id);
  }

  async mostrarModalComentario() {
    return await this.modal.open();
  }

  cerrarModal() {
    this.comentario = '';
    this.modal.close();
  }

  agregarComentario() {

    if (!this.album?.id) {
      this.modal.close();
      this.toastr.error(
        'Debe seleccionar un álbum primero.',
        'Operación inválida'
      );
      return;
    }

    this.albumService
      .agregarComentario(this.album.id, this.comentario.trim(), this.token)
      .subscribe((respuesta) => {
        if (respuesta && respuesta.data) {
          this.modal.close();
          this.comentario = '';
          this.toastr.success(
            'El comentario fue agregado satisfactoriamente',
            'Comentario agregado'
          );
          return;
        }
        this.toastr.error(
          'Ocurrió un error agregando el comentario. Intenta de nuevo, por favor.',
          'Error al comentar'
        );
      });
  }

  getDuracion(cancion: Cancion): string {
    const { minutos = 0, segundos = 0 } = cancion;
    return `${this.getNumeroConCero(minutos)}:${this.getNumeroConCero(
      segundos
    )}`;
  }

  getNumeroConCero(num: number): String {
    return num < 10 ? `0${num}` : num.toString();
  }

  getComentarioFormValido() {
    return !this.comentarioForm.invalid && this.comentario.trim().length > 0;
  }
}
