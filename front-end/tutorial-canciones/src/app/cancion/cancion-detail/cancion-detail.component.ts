import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  ViewChild,
  SimpleChanges,
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { ModalComponent } from 'src/app/components/modal/modal.component';
import { ModalConfig } from 'src/app/components/modal/modal.config';
import { Cancion } from '../cancion';
import { CancionService } from '../cancion.service';

@Component({
  selector: 'app-cancion-detail',
  templateUrl: './cancion-detail.component.html',
  styleUrls: ['./cancion-detail.component.scss'],
})
export class CancionDetailComponent implements OnInit {
  @ViewChild('modal') private modal: ModalComponent;

  @Input() cancion: Cancion;
  @Output() deleteCancion = new EventEmitter();

  userId: number;
  token: string;

  usuariosCompartidos: string = '';
  usuariosCompartidosPrev: string = '';
  usuariosCompartidosForm: FormGroup;
  cancionCompartida: Boolean = false;
  compartirCancionError: string;

  public modalConfig: ModalConfig = {
    modalTitle: 'Compartir Canción',
  };

  constructor(
    private router: ActivatedRoute,
    private routerPath: Router,
    private formBuilder: FormBuilder,
    private toastr: ToastrService,
    private cancionService: CancionService
  ) {}

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId);
    this.token = this.router.snapshot.params.userToken;
    this.usuariosCompartidosForm = this.formBuilder.group({
      comentario: ['', [Validators.required]],
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.cancion.currentValue?.id) {
      this.consultarUsuariosCompartidos();
    }
  }

  consultarUsuariosCompartidos() {
    this.cancionCompartida = false;
    this.usuariosCompartidosPrev = '';

    if (!this.cancion?.id || this.cancion?.compartida) {
      return;
    }
    this.cancionCompartida = false;
    this.usuariosCompartidosPrev = '';
    this.cancionService
      .consultarUsuariosCompartidos(this.cancion.id, this.token)
      .subscribe((response) => {
        if (
          response &&
          Array.isArray(response.usuarios_compartidos) &&
          response.usuarios_compartidos.length > 0
        ) {
          this.cancionCompartida = true;
          this.usuariosCompartidosPrev =
            response.usuarios_compartidos.join(',');
        }
      });
  }

  eliminarCancion() {
    this.deleteCancion.emit(this.cancion.id);
  }

  goToEdit() {
    this.routerPath.navigate([
      `/canciones/edit/${this.cancion.id}/${this.userId}/${this.token}`,
    ]);
  }

  async compartirCancion() {
    this.modalConfig.modalTitle = `Compartir Canción ${this.cancion.titulo}`;
    return await this.modal.open();
  }

  getUsuariosCompartirValido() {
    return (
      !this.usuariosCompartidosForm.invalid &&
      this.usuariosCompartidos &&
      this.usuariosCompartidos.trim().length > 0
    );
  }

  cerrarModal() {
    this.usuariosCompartidos = '';
    this.compartirCancionError = '';
    this.modal.close();
  }

  agregarUsuarios() {
    if (!this.cancion?.id) {
      this.modal.close();
      this.toastr.error(
        'Debe seleccionar una canción primero.',
        'Operación inválida'
      );
      return;
    }

    if (this.usuariosCompartidos === ""){
      this.compartirCancionError = 'Debes escribir el nombre de al menos un usuario para compartir';
      this.toastr.error(this.compartirCancionError, 'Error al compartir');

      return
    }

    let listaUsuarios:Array<string> = [];
    if (this.usuariosCompartidosPrev.trim().length > 0) {
      listaUsuarios = [...this.usuariosCompartidosPrev.trim().split(',')];
    }

    listaUsuarios = [
      ...listaUsuarios,
      ...this.usuariosCompartidos.trim().split(','),
    ];

    this.cancionService
      .compartirCancion(this.cancion.id, listaUsuarios, this.token)
      .subscribe(
        (respuesta) => {
          if (respuesta) {
            this.modal.close();
            this.usuariosCompartidos = '';
            this.toastr.success(
              'La canción se compartió con tus amigos',
              'Canción compartida'
            );
            this.consultarUsuariosCompartidos();
            return;
          }
          this.toastr.error(
            'Ocurrió un error compartiendo la canción. Intenta de nuevo, por favor.',
            'Error al compartir'
          );
        },
        (err) => {
          this.toastr.error(err.error, 'Error al compartir');
          this.compartirCancionError = err.error;
        }
      );
  }
}
