import {
  Component,
  Input,
  OnInit,
  Output,
  EventEmitter,
  ViewChild,
  SimpleChanges,
} from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AlbumService } from '../album.service';
import { Album, Cancion, Comentario } from '../album';

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
  @ViewChild('modalCompartir') private modalCompartir: ModalComponent;

  @Input() album: Album;
  @Output() deleteAlbum = new EventEmitter();

  usuariosCompartidos: string = '';
  usuariosCompartidosPrev: string = '';
  compartirAlbumError: string;
  comentarioForm: FormGroup;
  usuariosCompartidosForm: FormGroup;
  comentario: string;
  albumCompartido: boolean = false;

  userId: number;
  token: string;

  comentarios: Array<Comentario> = [];

  public modalConfigCompartir: ModalConfig = {
    modalTitle: 'Compartir Álbum',
  };

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
    this.usuariosCompartidosForm = this.formBuilder.group({
      usuarios_compartidos: ['', [Validators.required]],
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.album.currentValue?.id) {
      this.consultarComentariosAlbum();
      this.consultarUsuariosCompartidos();
    }
  }

  consultarComentariosAlbum() {
    if (!this.album?.id) {
      return;
    }
    this.albumService.getAlbumComments(this.album.id, this.token).subscribe(comentarios => {
      this.comentarios = comentarios;
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

  async compartirAlbum() {
    this.modalConfigCompartir.modalTitle = `Compartir Álbum ${this.album.titulo}`;
    return this.modalCompartir.open();
  }

  eliminarAlbum() {
    this.deleteAlbum.emit(this.album.id);
  }

  async mostrarModalComentario() {
    return this.modal.open();
  }

  cerrarModal() {
    this.comentario = '';
    this.modal.close();
  }

  cerrarModalCompartir() {
    this.usuariosCompartidos = '';
    this.compartirAlbumError = '';
    this.modalCompartir.close();
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
          this.consultarComentariosAlbum();
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

  agregarUsuarios() {
    if (!this.album?.id) {
      this.modalCompartir.close();
      this.toastr.error(
        'Debe seleccionar un álbum primero.',
        'Operación inválida'
      );
      return;
    }

    let listaUsuarios:Array<string> = [];
    if (this.usuariosCompartidosPrev.trim().length > 0) {
      listaUsuarios = [...this.usuariosCompartidosPrev.trim().split(',')];
    }

    listaUsuarios = [
      ...listaUsuarios,
      ...this.usuariosCompartidos.trim().split(','),
    ];

    this.albumService
      .compartirAlbum(this.album.id, listaUsuarios, this.token)
      .subscribe(
        (respuesta) => {
          if (respuesta) {
            this.modalCompartir.close();
            this.usuariosCompartidos = '';
            this.toastr.success(
              'El aĺbum se compartió con tus amigos',
              'Canción compartida'
            );
            this.consultarUsuariosCompartidos();
            return;
          }
          this.toastr.error(
            'Ocurrió un error compartiendo el álbum. Intenta de nuevo, por favor.',
            'Error al compartir'
          );
        },
        (err) => {
          this.toastr.error(err.error, 'Error al compartir');
          this.compartirAlbumError = err.error;
        }
      );
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

  getUsuariosCompartirValido() {
    return (
      !this.usuariosCompartidosForm.invalid &&
      this.usuariosCompartidos &&
      this.usuariosCompartidos.trim().length > 0
    );
  }

  consultarUsuariosCompartidos() {
    if (!this.album?.id) {
      return;
    }
    this.albumCompartido = false;
    this.usuariosCompartidosPrev = '';
    this.albumService
      .consultarUsuariosCompartidos(this.album.id, this.token)
      .subscribe((response) => {
        if (
          response &&
          Array.isArray(response.usuarios_compartidos) &&
          response.usuarios_compartidos.length > 0
        ) {
          this.albumCompartido = true;
          this.usuariosCompartidosPrev =
            response.usuarios_compartidos.join(',');
        }
      });
  }
}
